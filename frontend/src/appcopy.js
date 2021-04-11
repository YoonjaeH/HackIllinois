import './App.css';
import React,{useState, useEffect} from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';

function App({google}) {
   useEffect(() => { document.body.style.backgroundColor = '#252627' }, [])
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
                containerStyle = {{left: 10, right:0,position: 'absolute', width:'70%', height : '72%'}}
                initialCenter={
                  {
                    lat:39.8097343, 
                    lng: -98.5556199
                  }
                }>

              </Map>
            </div>
            <div id="space"></div>
            <div id="list">
              list in descending order here!
            </div>
            
      </div>
    </div>
  );
}

// export default App;
export default GoogleApiWrapper({
  apiKey:'AIzaSyDanli18HUvTuLM8XdREveskQMPF5EI3ng'
})(App);
