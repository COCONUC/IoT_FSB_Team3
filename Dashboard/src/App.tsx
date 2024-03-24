/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState, useRef } from "react";
import mqtt from "mqtt";
import "./App.css";
import ChartJS from "./Chart";
import PopUp from "./PopUp";
import { Slider } from "@mui/material";

const sensorTopics = [
  "group3/feeds/V1/temp",
  "group3/feeds/V1/humid",
  "group3/feeds/V1/r1",
  "group3/feeds/V1/r2",
  "group3/feeds/V1/r3",
];
const buttonTopics = ["group3/feeds/V2/r1", "group3/feeds/V2/r2", "group3/feeds/V2/r3"];

function App() {
  const [temp, setTemp] = useState("");
  const [humid, setHumid] = useState("");
  const [r1Switch, setR1Switch] = useState(false);
  const [r2Switch, setR2Switch] = useState(false);
  const [r3Switch, setR3Switch] = useState(false);
  const [tempHistory, setTempHistory] = useState<number[]>([]);
  const [humidHistory, setHumidHistory] = useState<number[]>([]);
  const [chartLimit, setChartLimit] = useState(20);
  const mqttClient = useRef<any>(null);
  const [dataset, setDataset] = useState([{ temp: 0, humid: 0, time: 1 }]);

  useEffect(() => {
    mqttClient.current = mqtt.connect("wss://dinhhn:0337221555@mqtt.ohstem.vn:8084", {
      clean: true,
      connectTimeout: 4000,
      clientId: "dinhhn:0337221555",
      username: "group3",
      password: "ngoansangdinh",
    });

    mqttClient.current.on("connect", () => {
      sensorTopics.map((topic: string) => {
        mqttClient.current.subscribe(topic, (err: any) => {
          if (!err) {
            console.log(`Subscribe ${topic} success`);
          } else console.log(`Subscribe ${topic} failed: `, err);
        });
      });
      buttonTopics.map((topic: string) => {
        mqttClient.current.subscribe(topic, (err: any) => {
          if (!err) {
            console.log(`Subscribe ${topic} success`);
          } else console.log(`Subscribe ${topic} failed: `, err);
        });
      });
    });

    mqttClient.current.on("error", (error: string) => {
      console.log("MQTT get error:", error);
    });

    mqttClient.current.on("message", (topic: string, message: Buffer) => {
      switch (topic) {
        case sensorTopics[0]:
          setTemp(message.toString());
          setTempHistory((prevHistory) => [...prevHistory, parseFloat(message.toString())]);
          break;
        case sensorTopics[1]:
          setHumid(message.toString());
          setHumidHistory((prevHistory) => [...prevHistory, parseFloat(message.toString())]);
          break;
        case sensorTopics[2]:
          setR1Switch(message.toString() === "True");
          break;
        case sensorTopics[3]:
          setR2Switch(message.toString() === "True");
          break;
        case sensorTopics[4]:
          setR3Switch(message.toString() === "True");
          break;
      }
      // console.log(`Message from topic ${topic}: `, message.toString())
    });
    return () => {
      mqttClient.current.end();
    };
  }, []);

  useEffect(() => {
    let data =
      tempHistory.length > 0
        ? tempHistory.map((value, index) => ({
            temp: value,
            humid: humidHistory[index] ?? 0,
            time: index + 1,
          }))
        : [{ temp: 0, humid: 0, time: 1 }];
    const startIndex = data.length - chartLimit
    if (data.length > chartLimit) data = data.slice(startIndex > 0 ? startIndex : 0);
    setDataset(data);
  }, [tempHistory.length, humidHistory.length, tempHistory, humidHistory, chartLimit]);

  const onClickR1 = () => {
    mqttClient.current.publish(buttonTopics[0], r1Switch ? "0" : "1");
  };
  const onClickR2 = () => {
    mqttClient.current.publish(buttonTopics[1], r2Switch ? "0" : "1");
  };
  const onClickR3 = () => {
    mqttClient.current.publish(buttonTopics[2], r3Switch ? "0" : "1");
  };

  return (
    <>
      <div className="container">
        <h3>DASHBOARD IOT TEAM 3</h3>
        <div className="d-flex">
          <div className="temp">
            <img width="80px" src="temp.png" />
            <span>{Math.floor(parseFloat(temp) * 100) / 100} °C</span>
          </div>
          <div className="humid">
            <img width="80px" src="viscosity.png" />
            <span>{Math.floor(parseFloat(humid) * 100) / 100} %</span>
          </div>
        </div>
        <div className="popup">
          <PopUp />
        </div>
        <ChartJS dataset={dataset} />
        <Slider
          aria-label="Limit items"
          getAriaValueText={(value: number) => `${value} items`}
          onChange={(_e, value) => setChartLimit(value as number)}
          defaultValue={20}
          step={5}
          min={5}
          max={50}
          valueLabelDisplay="auto"
          marks={[
            {
              value: 5,
              label: "5 times",
            },
            {
              value: 50,
              label: "50 times",
            },
          ]}
        />
        <div className="card">
          <div className="d-flex">
            <div>
              <input type="checkbox" checked={r1Switch} />
              <label onClick={onClickR1}></label>
            </div>
            <div>
              <input type="checkbox" checked={r2Switch} />
              <label onClick={onClickR2}></label>
            </div>
            <div>
              <input type="checkbox" checked={r3Switch} />
              <label onClick={onClickR3}></label>
            </div>
          </div>
          <div className="d-flex">
            <p>R1 Switch</p>
            <p>R2 Switch</p>
            <p>R3 Switch</p>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
