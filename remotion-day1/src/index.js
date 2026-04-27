import {registerRoot} from 'remotion';
import {RemotionRoot} from './Root';

// Remotion 的入口文件。
// registerRoot() 会告诉 Remotion 去哪里读取所有 Composition 定义。
registerRoot(RemotionRoot);
