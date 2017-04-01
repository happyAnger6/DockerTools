log_debug=4
log_info=3
log_warn=2
log_err=1
log_exit=0

debug_log()
{
	if [ $debug_flag -gt $log_debug ]
	then
		echo "[DEBUG]log:[ $1 ]"
	fi
}

info_log()
{
	if [ $debug_flag -gt $log_info ]
	then
		echo "[INFO]log:[ $1 ]"
	fi
}

warn_log()
{
	if [ $debug_flag -gt $log_warn ]
	then
		echo "[WARN]log:[ $1 ]"
	fi
}

err_log()
{
	if [ $debug_flag -gt $log_err ]
	then
		echo "[ERR]log:[ $1 ]"
	fi
}

exit_log()
{
	if [ $debug_flag -gt $log_exit ]
	then
		echo "[EXIT]log:[ $1 ]"
		exit 1
	fi
}
