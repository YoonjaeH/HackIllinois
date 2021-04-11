import './App.css';
import React,{useState, useEffect} from 'react';
import { Map, GoogleApiWrapper, Circle, Marker } from 'google-maps-react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { makeStyles } from '@material-ui/core/styles';

const test = [{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},
{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},
{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},{"state":"Alaska", "number":12},]

const useStyles = makeStyles((theme) => ({
  root: {
    position: 'relative',
    overflow: 'auto',
    height: "60vh",
    backgroundColor : '#202020'
  },
}));

function App({google}) {
  const statVisible = useState({});
  const classes = useStyles();
   useEffect(() => { document.body.style.backgroundColor = '#252627'}, [])
  return (
    <div className="App"> 
      <div id="header">
        <h4>Number of Hate Crimes againt Racial Minorities in U.S. by States</h4>
        <p id="description">
          Hackathon
        </p>
      </div>
      <div id="app-container">
           <div id="map">
              <Map 
                google = {google}
                zoom = {5}
                containerStyle = {{left: '2%', right:0,position: 'absolute', width:'70%', height : '72%'}}
                initialCenter={
                  {
                    lat:39.8097343, 
                    lng: -98.5556199
                  }
                }>
                  <Circle radius ={30000} 
                  center={{lat:39.7010784, lng: -90.4740999}}
                  strokeColor='transparent'
                  strokeOpacity={0}
                  strokeWeight={5}
                  onClick={() => console.log('click')}
                  onMouseover={(props) => console.log(props.center)}
                  fillColor='red'
                  fillOpacity={0.6}/>
              </Map>
            </div>
            <div id="space"></div>
            <div id="list">
              <h4 style={{marginBottom: '1rem', fontSize: '30px'}}>Past Occurence</h4>
              <List  className = {classes.root}>
                {test.map(({state, number})=>(
                  <ListItem key ={state}>
                    <ListItemText primary={state + ": " + number}/>
                  </ListItem>
                ))}
              </List>
            </div>
            
      </div>
    </div>
  );
}

// export default App;
export default GoogleApiWrapper({
  apiKey:'AIzaSyDanli18HUvTuLM8XdREveskQMPF5EI3ng'
})(App);
