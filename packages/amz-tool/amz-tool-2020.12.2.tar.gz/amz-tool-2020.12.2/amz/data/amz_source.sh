# Repo Details
export AMZ_ROOT=''
export AMZ_DATA=''
export AMZ_LINT=''

# Auto source ROS setup bash
if [ '$AMZ_ROOT' != '' ] && [[ -f $AMZ_ROOT/devel/setup.bash ]]
then
    source $AMZ_ROOT/devel/setup.bash
fi

# Aliases

## Utilities
alias amz_ssh_pilatus="ssh amz@10.33.0.2 -X"
alias amz_export_ros_pilatus="export ROS_MASTER_URI=http://10.33.0.2:11311"
alias amz_monitoring="export ROS_MASTER_URI=http://10.33.0.2:11311 && rosrun monitoring_display node_start.py --columns 4"
