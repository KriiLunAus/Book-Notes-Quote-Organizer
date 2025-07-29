import './App.scss'
import {fetchAuthors, fetchBooks, fetchJSON, fetchQuoteTags} from "../../utils/fetchFromBack.js"
import { useEffect } from 'react'

function App() {

    useEffect(()=>{
        // fetchAuthors()
        // fetchBooks()
        // fetchJSON()
        // fetchQuoteTags()
    },[])

return (<>
<div style={{backgroundColor:"red", width: "10px", height:"10px"}}></div>
</>)
}

export default App
