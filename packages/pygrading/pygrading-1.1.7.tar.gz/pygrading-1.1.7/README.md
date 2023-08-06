<h1>
    Pygrading
</h1>


CourseGrading(希冀)信息类专业教学与科研一体化平台开发用Python工具包

<p>
	<a href="http://www.educg.net/">
		<img src="https://img.shields.io/badge/site-CG-red" alt="Official Site">
	</a>
	<a href="https://pypi.org/project/pygrading/">
		<img src="https://img.shields.io/badge/pypi-v1.1.7-orange" alt="Pypi package">
	</a>
	<a href='https://pygrading.readthedocs.io/en/latest/?badge=latest'>
		<img src='https://readthedocs.org/projects/pygrading/badge/?version=latest' alt='Documentation Status' />
	</a>
	<a href="https://github.com/PhenomingZ/PyGrading/blob/master/LICENSE">
		<img src="https://img.shields.io/github/license/PhenomingZ/PyGrading" alt="GitHub license">
	</a>
</p>

<p>
	<a href="#what-is-it">What is it</a> •
	<a href="#install">Install</a> •
	<a href="#quick-start">Quick Start</a> •
	<a href="#change-log">Change Log</a> •
	<a href="#faq">FAQ</a> •
	<a href="http://www.educg.net/" target="_blank">CG Site</a>
</p>

<h6>Made by Charles Zhang • :globe_with_meridians: <a href="https://gitlab.educg.net/zhangmingyuan/PyGrading">https://gitlab.educg.net/zhangmingyuan/PyGrading</a></h6>

## What is it

**希冀平台** 全面支撑计算机、大数据、人工智能、集成电路、信息安全、机器人、金融科技、区块链等专业建设。 基于平台建成了涵盖实验、质量指标及过程控制的完整在线实验体系，实现了“任何人、任何时间、任何地点均能开展实验学习”的目标。

**通用评测** 是一个通用的自动评测框架，基于该框架可以定制开发任何自己需要的自动评测内核。

**PyGrading工具包** 目前该工具包包含以下功能：
1. 支持CourseGrading平台通用评测内核快速构建；
2. 支持适用于通用评测题、云桌面环境和Jupyter实验环境的评测结果JSON串的快速生成；
2. 支持HTML标签文本内容的快速生成，绝对好用的HTML生成工具；

希望使用本工具能够提高大家的工作效率，祝各位开发顺利！

## Install

使用pip可以轻松安装PyGrading：

```bash
pip install pygrading
```

PyGrading的运行环境要求 **Python >= 3.5**，不支持Python2。

## Quick Start

下面从一段简单的代码开始，使用PyGrading创建一个简单的通用评测内核：

```python
from pygrading import Job

# 创建一个任务对象
job = Job()

# 设定任务得分、评定结果和评语
job.score(100)
job.verdict("Accept") 
job.comment("Hello World")

# 输出评测结果
job.print()
```

这样就可以得到一个评测结果：
```json
{"verdict": "Accept", "score": "100", "rank": {"rank": "-1.0"}, "HTML": "enable", "comment": "Hello World"}
```

详细的使用手册请参考：[PyGrading开发文档](https://pygrading.readthedocs.io/en/latest/?badge=latest)

## Change Log

**v1.1.7 Change Log (2020.12.14)**  
1. 将`gg.utils.loge()`输出位置从`stdout`定向到了`stderr`。

**v1.1.6 Change Log (2020.12.14)**  
1. 为`gg.utils.loge()`绑定了环境变量`PYGRADING_DEBUG`，该变量为`True`时`loge`生效。

**v1.1.5 渲染更新 Change Log (2020.11.28)**  
1. 添加了Bootstrap4和Jinja2模板引擎的支持。
2. 支持了使用`gg.render_template()`方法渲染HTML模板！
3. 添加了默认渲染模板，该模板可使用`python -m pygrading init`创建，位于新建项目中的`templates/html/index.html`

**v1.0.1 Change Log (2020.11.24)**  
1. 去除了渲染结果时默认使用`str2html`的特性，因为其可能会导致JS失效。

**v1.0.0 正式版 Change Log (2020.11.21)**  
1. 重构了测试版底层架构，简化了导入步骤和部分包的使用方式。
2. 添加了命令行程序，支持使用`python -m pygrading init`创建项目模板。
3. 添加了多线程评测支持，高效利用服务器资源，提高评测效率。
4. 添加了评测超时控制功能，限制评测任务执行时间，防止卡死。
5. 添加了快速提取程序输出中评测指标的功能（键值对智能识别）。
6. 添加了图片转base64功能，快速生成图片展示元素。
7. 添加了携带环境变量执行评测功能（用于支撑需要读取不同环境变量的测试用例）。
8. 添加了评测指令执行静默模式，支持直接抛出评测指令的异常。
9. 添加了一键打包评测内核功能，打包好的评测内核可以通内核扩展上传。
10.  优化了评测过程函数的参数要求，支持不带参数的简单过程函数。

## FAQ

暂无内容
