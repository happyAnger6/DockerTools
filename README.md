# DockerTools
一系列docker脚本工具。
功能说明:

目录:pack_images:打包相关工具
log.sh:日志处理相关函数
tar_all_files.sh:将pack_files中的所有文件及依懒项递归打包成pack.tar
pack_files:要打包的工具,tar_all_files.sh会自动递归分析依懒项并打包.
