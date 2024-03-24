import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import ChatGPT from './ChatGPT';

function PopUp(){

    return (
        <>
        <Popup trigger=
            {<button><img width="50px" src="chat.png" alt="Chat" /></button>}
            position="right center">
            <ChatGPT/>
        </Popup>
        </>
    )
}

export default PopUp