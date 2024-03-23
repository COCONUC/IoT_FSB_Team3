import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import ChatGPT from './ChatGPT';
import { useEffect, useState, useRef } from 'react'

function PopUp(){

    const [message, setMessage] = useState('Nhiệt độ có phù hợp với sức khỏe không ?')

    // useEffect(() => {
    //     setMessage('ok')
    // },[])

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