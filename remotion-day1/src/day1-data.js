// 这一层只放视频内容数据，不放渲染逻辑。
// 这样 Day 2、Day 3 也能沿用同一套场景组件和字幕系统。

export const day1Overview = {
  title: 'Python Day 1',
  subtitle: '变量、函数、模块、容器、条件循环、入口写法',
  goal: '用一个 hello.py 跑通 Python 第一天最关键的基础能力。',
  stats: ['1 个 hello.py', '6 个核心概念', '从文档到代码'],
};

export const introScene = {
  title: '第一天教学视频',
  accent: '#38bdf8',
  durationInFrames: 180,
  narration: [
    {text: '今天这节，我们只做一件事，把 Python 第一天最重要的基础跑通。', frames: 60},
    {text: '你不用先背复杂语法，先看懂一个 hello.py，能自己运行起来就已经很够用了。', frames: 60},
    {text: '接下来我会用文档加代码，带你把 Day 1 拆成六个核心模块。', frames: 60},
  ],
};

export const checklistScene = {
  title: '今天学什么',
  accent: '#22c55e',
  durationInFrames: 180,
  callout: '先把最小可运行闭环建立起来',
  reasons: ['先能跑起来，再追求复杂度', 'hello.py 覆盖最基础必学能力', '后续 Day 2 到 Day 30 都建立在这些概念上'],
  narration: [
    {text: 'Day 1 重点不是知识越多越好，而是先建立最小可运行闭环。', frames: 60},
    {text: '所以你会先认识变量、函数、模块和常见容器类型。', frames: 60},
    {text: '再通过 if、for 和 main 入口，把整个脚本真正串起来。', frames: 60},
  ],
};

export const checklistItems = [
  '变量和常见数据类型',
  '字符串处理与类型转换',
  '函数和参数返回值',
  '模块导入与代码复用',
  'list / dict / tuple / set',
  'if、for、main 入口写法',
];

export const sections = [
  {
    title: '1. 变量和基础类型',
    concept: '给数据起名字，先分清值和类型。',
    points: [
      '变量就是给数据起名字',
      '先认识 str、int、float、bool、None',
      '用 type() 看变量的实际类型',
    ],
    chips: ['str', 'int', 'float', 'bool', 'None'],
    code: [
      'course_name = "Python Day 1"',
      'study_minutes = 90',
      'progress_score = 7.5',
      'has_started = True',
      'next_topic = None',
      'print(type(course_name).__name__)',
    ],
    accent: '#7dd3fc',
    durationInFrames: 180,
    narration: [
      {text: '第一步先别急着写复杂逻辑，你要先理解变量就是给数据起名字。', frames: 60},
      {text: '在 Day 1 里，你至少要认识字符串、整数、浮点数、布尔值和 None。', frames: 60},
      {text: '然后用 type 看一眼真实类型，后面写接口时你才不会把值用混。', frames: 60},
    ],
  },
  {
    title: '2. 字符串和类型转换',
    concept: '真实后端里，输入大多数先以字符串的形式出现。',
    points: [
      '后端里经常要先清洗字符串',
      '常见方法有 strip、split、replace、upper',
      '请求参数常常需要从字符串转成数字',
    ],
    chips: ['strip()', 'split()', 'replace()', 'upper()', 'int()', 'str()'],
    code: [
      'raw_name = "  minda python  "',
      'clean_name = raw_name.strip()',
      'print(clean_name.upper())',
      'print(clean_name.replace("python", "backend"))',
      'age_number = int("18")',
      'score_text = str(99)',
    ],
    accent: '#86efac',
    durationInFrames: 180,
    narration: [
      {text: '接下来是特别实用的一块，字符串处理和类型转换。', frames: 60},
      {text: '因为后端收到的请求参数，很多时候最开始都是字符串。', frames: 60},
      {text: '所以你要会清洗文本，也要会把十八这样的字符串转成真正的数字。', frames: 60},
    ],
  },
  {
    title: '3. 容器类型',
    concept: '一组数据、一条记录、固定值、去重，这四种需求经常出现。',
    points: [
      'list 保存一组有顺序、可修改的数据',
      'dict 适合描述一个对象',
      'tuple 表示固定数据，set 常用来去重',
    ],
    chips: ['list', 'dict', 'tuple', 'set'],
    code: [
      'tasks = ["安装 Python", "创建虚拟环境", "运行 hello.py"]',
      'student = {"name": "Minda", "goal": "学习 Python 后端"}',
      'screen_size = (1920, 1080)',
      'tags = {"python", "python", "fastapi"}',
      'print(len(tasks))',
    ],
    accent: '#f9a8d4',
    durationInFrames: 180,
    narration: [
      {text: '然后你要认识四个最常见的容器类型。', frames: 60},
      {text: '列表适合放一组任务，字典适合描述一个对象，元组适合固定数据。', frames: 60},
      {text: '集合则很适合去重，这些都是后面写业务代码时会反复碰到的工具。', frames: 60},
    ],
  },
  {
    title: '4. 条件和循环',
    concept: '代码开始有判断和重复，脚本才真正像脚本。',
    points: [
      'if / else 根据条件执行不同逻辑',
      'Day 1 先重点掌握 for',
      'enumerate() 可以同时拿到序号和元素',
    ],
    chips: ['if', 'else', 'for', 'enumerate()'],
    code: [
      'if len(tasks) >= 4:',
      '    print("今天的任务已经比较完整了。")',
      'for index, task in enumerate(tasks, start=1):',
      '    print(f"第 {index} 个任务: {task}")',
    ],
    accent: '#fdba74',
    durationInFrames: 180,
    narration: [
      {text: '有了数据之后，就该让代码开始做判断和重复执行。', frames: 60},
      {text: 'if 和 else 用来分支，for 用来遍历，Day 1 你先把 for 用熟就很好。', frames: 60},
      {text: '再配合 enumerate，你就可以一边拿序号，一边拿列表里的内容。', frames: 60},
    ],
  },
  {
    title: '5. 函数和模块',
    concept: '把重复逻辑封装成函数，再拆到独立文件里复用。',
    points: [
      '函数把重复逻辑封装起来',
      '参数是输入，返回值是输出',
      '一个 .py 文件就是一个模块，可以 import 使用',
    ],
    chips: ['def', 'return', 'import', 'module'],
    code: [
      'from test import build_learning_profile, format_greeting',
      '',
      'def format_greeting(name: str) -> str:',
      '    return f"你好，{name}，欢迎开始 Python 第一天学习。"',
      '',
      'profile = build_learning_profile(STUDENT_NAME, "Python 后端")',
    ],
    accent: '#c4b5fd',
    durationInFrames: 180,
    narration: [
      {text: '接着你会看到函数和模块这两个概念是怎么连在一起的。', frames: 60},
      {text: '函数负责封装逻辑，参数是输入，返回值是输出。', frames: 60},
      {text: '而 test.py 这种独立文件就是模块，可以被 hello.py import 进来复用。', frames: 60},
    ],
  },
  {
    title: '6. 入口写法',
    concept: 'main 负责组织执行顺序，入口判断决定何时真正运行。',
    points: [
      '直接运行当前文件时，main() 才执行',
      '如果文件被 import，就不会自动执行',
      '这是 Python 项目里非常常见的组织方式',
    ],
    chips: ['main()', '__name__', '__main__'],
    code: [
      'def main() -> None:',
      '    show_basic_types()',
      '    show_string_and_conversion_examples()',
      '    tasks = show_containers()',
      '    show_control_flow(tasks)',
      '',
      'if __name__ == "__main__":',
      '    main()',
    ],
    accent: '#fcd34d',
    durationInFrames: 180,
    narration: [
      {text: '最后一个关键点，是 Python 里非常经典的入口写法。', frames: 60},
      {text: 'main 负责把流程按顺序串起来，而 if name 等于 main 用来判断是不是直接运行当前文件。', frames: 60},
      {text: '这个模式以后你会在很多正式项目里看到，所以 Day 1 一定要先认熟。', frames: 60},
    ],
  },
];

export const runScene = {
  title: '运行演示',
  accent: '#f59e0b',
  durationInFrames: 150,
  steps: [
    '进入 2026-04-16-day1 目录',
    '如果需要，先激活虚拟环境',
    '执行 python hello.py',
    '观察输出的基础类型、容器、循环和模块导入结果',
  ],
  terminalLines: [
    'cd 2026-04-16-day1',
    'python hello.py',
    '',
    'Python Day 1 学习示例开始',
    '=== 1. 基础数据类型 ===',
    'course_name = Python Day 1, type = str',
    'study_minutes = 90, type = int',
    '=== 4. 函数和模块 ===',
    '你好，Minda，欢迎开始 Python 第一天学习。',
  ],
  narration: [
    {text: '到这里，最关键的一步就是把它真的跑起来。', frames: 50},
    {text: '进入 Day 1 目录后执行 python hello.py，你就能看到前面这些知识点被依次打印出来。', frames: 50},
    {text: '只要你能独立完成这一步，第一天就已经不算白学。', frames: 50},
  ],
};

export const summaryScene = {
  title: '结尾总结',
  accent: '#a78bfa',
  durationInFrames: 180,
  completionItems: [
    '能看懂一个最基础的 Python 文件',
    '能自己写函数并调用',
    '知道列表和字典分别适合存什么数据',
    '知道 if 和 for 是干嘛的',
    '知道 if __name__ == "__main__" 的作用',
    '能独立运行 python hello.py',
  ],
  practiceItems: [
    '把 STUDENT_NAME 改成你自己的名字',
    '给任务列表再加 2 条任务',
    '自己再写一个统计任务数量的函数',
  ],
  nextStep: 'Day 2 可以继续衔接类、异常、类型注解和异步基础。',
  narration: [
    {text: '如果你现在已经能看懂 hello.py 的结构，并且知道每一段在干嘛，Day 1 就算过关。', frames: 60},
    {text: '接下来最好的练法，是改名字、补任务，再自己多写一个小函数。', frames: 60},
    {text: '等这些都顺了，再去接 Day 2 的类、异常和类型注解，你会轻松很多。', frames: 60},
  ],
};

export const voiceoverSections = [
  {title: '开场', lines: introScene.narration.map((item) => item.text)},
  {title: '今天学什么', lines: checklistScene.narration.map((item) => item.text)},
  ...sections.map((section) => ({title: section.title, lines: section.narration.map((item) => item.text)})),
  {title: '运行演示', lines: runScene.narration.map((item) => item.text)},
  {title: '结尾总结', lines: summaryScene.narration.map((item) => item.text)},
];

export const totalDurationInFrames =
  introScene.durationInFrames +
  checklistScene.durationInFrames +
  sections.reduce((total, section) => total + section.durationInFrames, 0) +
  runScene.durationInFrames +
  summaryScene.durationInFrames;
