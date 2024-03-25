import Popup from "reactjs-popup";
import "reactjs-popup/dist/index.css";
import ChatGPT from "./ChatGPT";
import Alarm from "./alarm";
import { useState } from "react";

interface Props {
  temp: string;
  humid: string;
}

function PopUp(props: Props) {
  const [trigger, setTrigger] = useState(false);

  return (
    <>
      {/* <button onClick={() => setTrigger(!trigger)}>
        {trigger ? <img width="50px" src="chat_triggered.png" alt="Chat" /> : <img width="50px" src="chat.png" alt="Chat" />}
      </button>
      {trigger && <Alarm {...props} />} */}

      <Popup
        trigger={
          <button>
            <img width="50px" src="chat.png" alt="Chat" />
          </button>
        }
        position="right top"
      >
        <ChatGPT {...props} />
      </Popup>
    </>
  );
}

export default PopUp;
