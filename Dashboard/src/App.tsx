import { useEffect, useState, useRef } from 'react'
import mqtt from 'mqtt'
import './App.css'

const sensorTopics = ['group3/feeds/V1/temp', 'group3/feeds/V1/humid', 'group3/feeds/V1/r1', 'group3/feeds/V1/r2', 'group3/feeds/V1/r3']
const buttonTopics = ['group3/feeds/V2/r1', 'group3/feeds/V2/r2', 'group3/feeds/V2/r3']

function App() {
  const [temp, setTemp] = useState('')
  const [humid, setHumid] = useState('')
  const [r1Switch, setR1Switch] = useState(false)
  const [r2Switch, setR2Switch] = useState(false)
  const [r3Switch, setR3Switch] = useState(false)
  const [tempHistory, setTempHistory] = useState<number[]>([])
  const [humidHistory, setHumidHistory] = useState<number[]>([])
  const mqttClient = useRef<any>(null)

  useEffect(() => {
    mqttClient.current = mqtt.connect('wss://dinhhn:0337221555@mqtt.ohstem.vn:8084', {
      clean: true,
      connectTimeout: 4000,
      clientId: 'dinhhn:0337221555',
      username: 'yolo2907',
      password: 'abc123'
    })

    mqttClient.current.on('connect', () => {
      sensorTopics.map((topic: string) => {
        mqttClient.current.subscribe(topic, (err: any) => {
          if (!err) {
            console.log(`Subscribe ${topic} success`)
          } else console.log(`Subscribe ${topic} failed: `, err)
        })
      })
      buttonTopics.map((topic: string) => {
        mqttClient.current.subscribe(topic, (err: any) => {
          if (!err) {
            console.log(`Subscribe ${topic} success`)
          } else console.log(`Subscribe ${topic} failed: `, err)
        })
      })
    })

    mqttClient.current.on('error', (error: string) => {
      console.log('MQTT get error:', error)
    })

    mqttClient.current.on('message', (topic: string, message: Buffer) => {
      switch (topic) {
        case sensorTopics[0]:
          setTemp(message.toString())
          setTempHistory((prevHistory) => [...prevHistory, parseFloat(message.toString())])
          break
        case sensorTopics[1]:
          setHumid(message.toString())
          setHumidHistory((prevHistory) => [...prevHistory, parseFloat(message.toString())])
          break
        case buttonTopics[2]:
          console.log(!!message.toString())
          setR1Switch(!!message.toString())
          break
        case buttonTopics[3]:
          console.log(!!message.toString())
          setR2Switch(!!message.toString())
          break
        case buttonTopics[5]:
          console.log(!!message.toString())
          setR2Switch(!!message.toString())
          break
      }
      // console.log(`Message from topic ${topic}: `, message.toString())
    })
    return () => {
      mqttClient.current.end()
    }
  }, [])

  useEffect(() => {
    // console.log(tempHistory)
  }, [tempHistory])

  useEffect(() => {
    // console.log(humidHistory)
  }, [humidHistory])

  const onClickR1 = () => {
    mqttClient.current.publish(buttonTopics[0], r1Switch ? '0' : '1')
  }
  const onClickR2 = () => {
    mqttClient.current.publish(buttonTopics[1], r2Switch ? '0' : '1')
  }
  const onClickR3 = () => {
    mqttClient.current.publish(buttonTopics[2], r3Switch ? '0' : '1')
  }

  return (
    <>
      <h1>DASHBOARD</h1>
      <div className='card'>
        <span>Temperature: {Math.round(parseFloat(temp) * 100) / 100} °C</span>
        <br />
        <span>Humidity: {Math.round(parseFloat(humid) * 100) / 100} %</span>
        <br />
        <button onClick={onClickR1}>R1 SWITCH: {r1Switch ? 'ON' : 'OFF'}</button>
        <br />
        <button onClick={onClickR2}>R2 SWITCH {r2Switch ? 'ON' : 'OFF'}</button>
        <br />
        <button onClick={onClickR3}>R3 SWITCH {r3Switch ? 'ON' : 'OFF'}</button>
      </div>
    </>
  )
}

export default App
