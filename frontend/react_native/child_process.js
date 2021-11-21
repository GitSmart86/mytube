import {spawn, kill} from 'react-native-childprocess';

let cmdID;

export async function start() {
  cmdID = await spawn('/sbin/ping', ['google.com'], {
    pwd: project.path,
    stdout: output => {
      console.log('>>>', output);
    },
  });
}

export async function stop() {
  kill(cmdID);
}
