# Human-posture-recognition-system-based-on-millimeter-wave-radar
基于毫米波雷达的人体姿态识别系统
程序使用PointNet++模型来识别人体姿态。训练使用的也是PointNet++模型，可以自行替换模型。但是识别会按照20\40\60\80个点云文件依次执行判断。同时勾选多个模型会导致识别依次进行，造成程序识别结果滞后显示。
硬件设备使用纳雷科技SR75雷达和创芯科技CAN盒子。
程序使用Python + ttk bootstrap + ttk 开发GUI。对静态姿态几乎没有识别能力。
attitude.txt里面保存的是训练的模型包含的姿态类型，如果你训练的模型姿态有所不同，务必检查Window.py、test_data.py、Posture_Recognition.py因为其中包含有模型识别的代码需要修改其中姿态的类型数量，同时修改attitude.txt。
系统的文件入口 ：Window.py
模型训练点云文件的预处理程序: PointNet model training data preprocessor.py
