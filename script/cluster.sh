#!/bin/bash
#! /bin/sh
#############################################
cd $(dirname `ls -l $0 | awk '{print $NF;}'`)/..
WK_DIR=`pwd`
WK_PRI_DIR=${WK_DIR}
##############################################
DEFAULT_CONF=${WK_PRI_DIR}/conf/default.conf
SRC_DIR=${WK_PRI_DIR}/src

##############################################
source ${DEFAULT_CONF}
##############################################

K=40
dt=20191016
hour=07
flag=1
iters=20

function prepare_dir(){
    LOG_AND_EXECUTE "hadoop fs -rmr $1 || true"
    LOG_AND_EXECUTE "hadoop fs -mkdir -p $1 || true"
    LOG_AND_EXECUTE "hadoop fs -chmod -R 777 $1"    ##要改
}



###初始化聚类中心#######################################
LOG_AND_EXECUTE "hadoop fs -cat ${OUTPUT}/* > ./lcf_vector"
/usr/bin/python2.7 ${SRC_DIR}/init_cluster.py ./lcf_vector $K > ./init_cluster
LOG_AND_EXECUTE "hadoop fs -rm  ${HDFS_ROOT}/init_cluster"
LOG_AND_EXECUTE "hadoop fs -put ./init_cluster ${HDFS_ROOT}"

###更新聚类中心#########################################
center_path="${HDFS_ROOT}/init_cluster"
data_path="/yongkun1/clusters/lcf_vector"
output_path="/yongkun1/clusters/update"

mapper_file="update_mapper.py"
reducer_file="update_reducer.py"

cmd_update_center="
    $HADOOP jar $HADOOP_STREAMING_JAR \
    -input $data_path \
    -output $output_path \
    -cacheArchive \"hdfs://yongkun1/VR/tools_python/Python.zip#Python\" \
    -mapper \"Python/bin/python $mapper_file\" \
    -reducer \"Python/bin/python $reducer_file\" \
    -file ${SRC_DIR}/${mapper_file} \
    -file ${SRC_DIR}/${reducer_file} \
    -cacheFile \"${center_path}#centers\" \
    -jobconf mapreduce.job.reduces=50 \
    -jobconf mapreduce.job.maps=100
"

LOG_AND_EXECUTE "hadoop fs -rmr  ${output_path}"
for((i=1;i<=${iters};i++));  
do   
    LOG_AND_EXECUTE "$cmd_update_center"
    LOG_AND_EXECUTE "hadoop fs -cat ${output_path}/* > ./new_cluster"
    ###更新结果和原来结果合并
    /usr/bin/python2.7 ${SRC_DIR}/update_clusetr.py ./new_cluster ./init_cluster $K > ./init_cluster 
    LOG_AND_EXECUTE "hadoop fs -rm  ${HDFS_ROOT}/init_cluster"
    LOG_AND_EXECUTE "hadoop fs -put ./init_cluster ${HDFS_ROOT}"
    LOG_AND_EXECUTE "hadoop fs -rmr  ${output_path}"
    LOG "$i"
done  

###################################################
mapper_file="predict_mapper.py"
reducer_file="predict_reducer.py"
output_path="/yongkun1/clusters/predict"

cmd_predict="
    $HADOOP jar $HADOOP_STREAMING_JAR \
    -input $data_path \
    -output $output_path \
    -cacheArchive \"hdfs://yongkun1/VR/tools_python/Python.zip#Python\" \
    -mapper \"Python/bin/python $mapper_file\" \
    -reducer \"Python/bin/python $reducer_file\" \
    -file ${SRC_DIR}/${mapper_file} \
    -file ${SRC_DIR}/${reducer_file} \
    -cacheFile \"${center_path}#centers\" \
    -jobconf mapreduce.job.reduces=50 \
    -jobconf mapreduce.job.maps=100
"
###############预测结果
LOG_AND_EXECUTE "hadoop fs -rmr  ${output_path}"
LOG_AND_EXECUTE "$cmd_predict"
LOG_AND_EXECUTE "hadoop fs -cat ${output_path}/* > ./predict"
