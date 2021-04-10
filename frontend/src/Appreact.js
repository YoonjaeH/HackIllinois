import './App.css';
import React,{useState} from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';
import Box from '@material-ui/core/Box';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme)=> ({
    root:{
        display:'flex',
        flexDirection:'column', 
        padding:0,
        margin:0
    },
    header:{
        margin: '2%',
        justifyContent:'center',
        backgroundColor:'white',
    },
    headerh4:{
        fontSize : '2rem',
        textAlign:'center'
    },
    body:{
        display: 'flex',
        backgroundColor:'green',
        flexDirection:'row',
        justifyContent:'flex-start',
        alignItems:'flex-start'
    },
    headerp:{
        fontSize:'1rem',
    },
    mapdiv:{
        flex:1
    },
    spacing:{
        flex:1
    },
    list:{
        flex:1
    }
}))
function App({google}) {
    const classes = useStyles();
    return(
        <Box className = {classes.root}>
            <div className = {classes.header}>
                <h4 className = {classes.headerh4}>Number of Hate Crimes againt Racial Minorities in U.S. by States</h4>
                <p className = {classes.headerp}>
                    Hackathon
                </p>
            </div>
            
            <div className = {classes.body}>
                <div className = {classes.mapdiv}>
                    <Map 
                    google = {google}
                    zoom = {5}
                    containerStyle={{
                        position: 'relative',  
                        width: '70%',
                        height:'65%',
                    }}
                    initialCenter={
                    {
                        lat:39.8097343, 
                        lng: -98.5556199
                    }
                    }>

                    </Map>
                </div>
                <div className = {classes.spacing}>
                </div>
                <div className = {classes.list}>
                    <h4>list</h4>
                </div>
                
            </div>  
        </Box>
    )
//   return (
//     <div className="App">
//       <div id="header">
//         <h4>Number of Hate Crimes againt Racial Minorities in U.S. by States</h4>
//         <p id="description">
//           short description goes here !!
//         </p>
//       </div>
//       <div id="app-container">
//             <div id="map">
//               <Map 
//                 google = {google}
//                 zoom = {5}
//                 style = {{width:'80%', height : '80%'}}
//                 initialCenter={
//                   {
//                     lat:39.8097343, 
//                     lng: -98.5556199
//                   }
//                 }>

//               </Map>
//             </div>
//             <div id="space"></div>
//             <div id="list">
//               list in descending order here!
//             </div>
//       </div>
//     </div>
//   );
}

// export default App;
export default GoogleApiWrapper({
  apiKey:'AIzaSyDanli18HUvTuLM8XdREveskQMPF5EI3ng'
})(App);
