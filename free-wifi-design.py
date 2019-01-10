######## 模块 ########
# WIFI 管理模块
	# 检查硬件支持
	# 状态监控
	# 开启/重启
	# 关闭

# 账户管理模块
	# 基本操作
		# 查询
		# 新建/更改
		# 删除
		# 选择
	# 底层操作
		# 预备配置（检查并确保配置文件存在）
		# 读取配置
		# 写出配置
		# 刷新配置
		# 检查格式（确保 ssid 和 key 的格式符合指定要求）

# 命令行模块
	# 映射表管理
		# 文本指令 ： 逻辑流程函数
	# 异常捕捉处理
		# 装饰器模式
	# 循环执行体
		# 指令接收+处理

# 监控模块
	# 职能要求
		# 监控 WIFI 运作状态并自动重启 WIFI
		# 作为后台进程运行
	# 运作机制
		# 每次 WIFI 关闭状态下用户手动启动 WIFI
			# 生成一个状态维护文件
				# 文件名由前缀+一串随机数组成，唯一标识每次未手动关闭过的 WIFI 作业
			# 启动后台监控进程
		# 后台进程启动后即独立运作
			# 每隔 15s 检查一次
				# 对应的状态维护文件还在就持续运作，否则自行退出
				# 如果 WIFI 中断则重启 WIFI

######## 流程 ########
# 脚本预处理
	# 脚本启动时检查硬件支持
		# 如果不支持直接给出提示并任意键退出
	# 检查并确保账户配置文件存在
		# 若不存在则新建
# 开启 WIFI
	# 读取并检查配置
	# 如果配置可用
		# 执行 WIFI 启动命令
		# 启动监控进程（如果已启动则跳过，不要重复启动）
	# 否则
		# 反映配置问题并提供指导
	# 返回
# 关闭 WIFI
	# 关闭监控进程
	# 执行 WIFI 关闭命令
# 显示 WIFI
	# 执行 WIFI 状态命令
# 显示账户配置
# 新增/更改账户
	# 检查 ssid 以及 key 的格式是否合规
	# 插入/修改指定 ssid 和 key
	# 刷新账户配置
	# 导出至本地
# 删除账户
	# 检查是否存在指定账户
	# 删除指定 ssid 及其 key
	# 刷新账户配置
	# 导出至本地
# 选择指定账户
	# 检查是否存在指定账户
	# 变更当前的选中的账户
	# 刷新账户配置
	# 导出至本地
# 手动开启监视进程
# 手动关闭监视进程

