/**
 * @format
 */

import {AppRegistry} from 'react-native';
import App from './App';
import {name as appName} from './app.json';

// 启用React Native Reanimated
import 'react-native-reanimated';

// 启用React Native Gesture Handler
import 'react-native-gesture-handler';

AppRegistry.registerComponent(appName, () => App);