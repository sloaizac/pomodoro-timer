import React from 'react';
import { StyleSheet, Text, View, Button, TextInput } from 'react-native';
import { vibrate } from './utils';

export default class App extends React.Component {
  state = {
    work_min: 1,
    work_sec: 0,
    break_min: 0,
    break_sec: 20,
    countMin: 0,
    countSeg: 0,
    pause: false,
    work: true,
  };

  componentDidMount() {
    this.reset();
    this.start();
  }

  reset = () => {
    this.setState({
      countMin: this.state.work_min,
      countSeg: this.state.work_sec,
      pause: false,
      work: true,
    });
  };

  start = () => {
    setInterval(this.countDown, 1000);
  };

  countDown = () => {
    if (!this.state.pause) {
      if (this.state.countMin === 0 && this.state.countSeg === 0) {
        if (this.state.work) {
          this.setState({
            countMin: this.state.break_min,
            countSeg: this.state.break_sec,
            work: false,
          });
        } else {
          this.setState({
            countMin: this.state.work_min,
            countSeg: this.state.work_sec,
            work: true,
          });
        }
        vibrate();
      } else if (this.state.countSeg === 0) {
        this.setState({
          countMin: this.state.countMin - 1,
          countSeg: 59,
        });
      } else {
        this.setState({
          countSeg: this.state.countSeg - 1,
        });
      }
    }
  };

  pause = () => {
    this.setState({
      pause: true,
    });
  };

  restart = () => {
    this.setState({
      pause: false,
    });
  };

  onChangeWork = time => {
    this.setState({
      work_min: parseInt(time),
    });
  };

  onChangeBreak = time => {
    this.setState({
      break_min: parseInt(time),
    });
  };

  render() {
    return (
      <View style={styles.container}>
        {this.state.work ? (
          <Text style={styles.title}>WORK TIME</Text>
        ) : (
          <Text style={styles.title}>BREAK TIME</Text>
        )}
        <Text style={styles.counter}>
          {('0' + this.state.countMin).slice(-2)}:
          {('0' + this.state.countSeg).slice(-2)}
        </Text>
        <View style={{display: 'flex', flexDirection: 'row'}}>
          {this.state.pause ? (
          <Button  onPress={this.restart} title="start" />
        ) : (
          <Button onPress={this.pause} title="pause" />
        )}
        </View>
        <Button style={styles.button} onPress={this.reset} title="reset" />
        <View style={styles.inputBox}>
          <Text style={styles.textTitle}>Work time:</Text>
          <TextInput
            style={styles.input}
            onChangeText={text => this.onChangeWork(text)}
            defaultValue="20"
            keyboardType={'numeric'}
          />
        </View>

        <View style={styles.inputBox}>
          <Text style={styles.textTitle}>Break time: </Text>
          <TextInput
            style={styles.input}
            onChangeText={text => this.onChangeBreak(text)}
            defaultValue="5"
            keyboardType={'numeric'}
          />
        </View>
        <Button onPress={this.reset} title="change" />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: '50%',
    marginBottom: 2,
  },
  counter: {
    fontSize: '100%',
    fontWeight: 'bold',
    margin: 2,
  },
  inputBox: {
    width: '100%',
    display: 'flex',
    flexDirection: 'row',
    padding: 5,
    height: '6%',
    marginLeft: 30,
    marginTop: 10
  },
  input: {
    borderColor: '#000',
    borderWidth: 1,
    height: '100%',
    width: '15%',
    marginLeft: 10,
    textAlign: 'center',
    fontSize: '20%',
  },
  textTitle: {
    fontSize: '20%',
    height: '100%',
    textAlign: 'center',
  },
});