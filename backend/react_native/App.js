import React, {useState} from 'react';
import {StyleSheet, Text, TextInput, View, Button} from 'react-native';
import {spawn, kill} from 'react-native-childprocess';

const App = () => {
  const [url, setUrl] = useState('');
  const [mode, setMode] = useState('');
  const [quality, setQuality] = useState('');
  const [childPython, setChildPython] = useState(null);

  async function start(argv) {
    let child = await spawn('python', ['backend/test.py', ...argv], {
      pwd: 'project.path',
      stdout: output => {
        console.log('>>>', output);
      },
      stderr: output => {
        console.log('>>>', output);
      },

      // childPython.stdout.on('data', data => {
      //   console.log(`stdout: ${data}`);
      // });

      // childPython.stderr.on('data', data => {
      //   console.error(`stderr: ${data}`);
      // });

      // childPython.stdout.on('close', exitCode => {
      //   console.log(`childPython closed with crash = ${exitCode}`);
      // });
    });

    setChildPython(child);
  }

  async function stop() {
    kill(childPython);
  }

  function handleSubmit() {
    // test.py( url, mode, quality )
    const argv = [
      'https://www.youtube.com/watch?v=aoMzOgiE7rY',
      'audio',
      'min',
    ];

    // const childPython = spawn('python', ['test.py', JSON.stringify(argv)]);
    const childPython = spawn('python', ['backend/test.py', ...argv]);
  }

  return (
    <>
      <View title="Input Url" style={styles.container}>
        <Text style={styles.text}>Url:</Text>
        <TextInput
          placeholder="https//:youtube.com/..."
          style={styles.input}
          onChangeText={value => setUrl(value)}
        />

        {/* {__dirname}
        {process.cwd()} */}

        <Text style={styles.text}>Mode:</Text>
        <TextInput
          placeholder="[ 'audio' | 'video' ]"
          style={styles.input}
          onChangeText={value => setMode(value)}
        />

        <Text style={styles.text}>Quality:</Text>
        <TextInput
          placeholder="[ 'max' | 'min' ]"
          style={styles.input}
          onChangeText={value => setQuality(value)}
        />

        <Button title="do something" onPress={handleSubmit} />
      </View>

      {/* <Section title="Debug">
        <DebugInstructions />
      </Section>
      <LearnMoreLinks /> */}
    </>
  );
};

const styles = StyleSheet.create({
  sectionContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: '600',
  },
  sectionDescription: {
    marginTop: 8,
    fontSize: 18,
    fontWeight: '400',
  },
  highlight: {
    fontWeight: '700',
  },
  container: {
    height: '100%',
    // backgroundColor: '#fffc',
    alignItems: 'center',
    justifyContent: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#777',
    padding: 8,
    margin: 10,
    width: 200,
  },
  text: {
    color: 'black',
  },
  buttonContainer: {
    marginTop: 20,
  },
});

export default App;
