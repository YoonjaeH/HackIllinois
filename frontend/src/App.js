import './App.css';
import React,{useState, useEffect} from 'react';
import { Map, GoogleApiWrapper, Circle, Marker } from 'google-maps-react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { makeStyles } from '@material-ui/core/styles';
import actualdata from './data/actual_data.json'
import predictdata from './data/predict_data.json'
import Slider from '@material-ui/core/Slider';
import GeoCenter from './const'
const useStyles = makeStyles((theme) => ({
  root: {
    position: 'relative',
    overflow: 'auto',
    height: "60vh",
    backgroundColor : '#202020'
  },
  slider:{
    marginLeft:'2%',
  }
}));

/**
 * Returns the radious and the hue of based on 
 * the prediction percentage of the state.
 * @param {Float} p the prediction percentage value between 0 and 1
 * @returns {Array} the radious and hue of the circle
 */
function pred_rad_and_hue(p) {
  const r = (2 * p + 2) * 10000;
  let g_comp = Math.abs(Math.floor(255 * (1 - p))).toString(16);
  let r_comp = Math.abs(Math.floor(255 * p)).toString(16);
  const b_comp = "00";
  if(g_comp.length ===3)
  {
    g_comp = g_comp.slice(1)
  }
  if(g_comp.length === 1)
  {
    g_comp = '0' + g_comp;
  }
  if(r_comp.length === 1)
  {
    r_comp = '0' + r_comp;
  }

  const h = r_comp + g_comp + b_comp;

  return { "rad" : r, "hue" : h}
}

function convertToKey(input) 
{
  let [month, date, year] = new Date(input).toLocaleDateString("en-US").split("/")
  if(date.length === 1)
  {
    date = '0' + date
  }
  if(month.length === 1)
  {
    month = '0' + month
  }
  return year + "-" + month + "-" + date
}

function nextDay(input, value)
{
  let temp = new Date(input)
  temp.setDate(temp.getDate()+value)
  let [month, date, year] =  temp.toLocaleDateString("en-US").split("/")
  if(date.length === 1)
  {
    date = '0' + date
  }
  if(month.length === 1)
  {
    month = '0' + month
  }
  return year + "-" + month + "-" + date
}

function App({google}) {
  const statVisible = useState({});
  const [mapArray, setMapArray]= useState([])
  const [listArray, setListArray] = useState([])
  const actualkeys = Object.keys(actualdata)
  const predictkeys = Object.keys(predictdata)
  const classes = useStyles();
  const actualStartDate = convertToKey(actualkeys[0])
  const actualEndDate = convertToKey(actualkeys[actualkeys.length - 1])
  const predictStartDate = convertToKey(predictkeys[0])
  const predictEndDate = convertToKey(actualkeys[predictkeys.length - 1])
   useEffect(() => {  document.body.style.backgroundColor = '#252627'}, [])

   const handleChange = (event, newValue)=>{
      const actualObj = actualdata[nextDay(actualStartDate, newValue)]
      const predictObj = predictdata[nextDay(predictStartDate, newValue)]
      console.log(actualObj, predictObj)
      const circleResult = Object.keys(actualObj).map((value, index, array)=>{
        const predictionError = (Math.abs((actualObj[value]+1) - (predictObj[value]+1)))/(actualObj[value]+1)
        const radHue = pred_rad_and_hue(predictionError)
        const [lati, longi] = GeoCenter[value]
        return (<Circle radius ={radHue['rad']} 
          center={{lat:lati, lng:(-1*longi)}}
          strokeColor='transparent'
          strokeOpacity={0}
          strokeWeight={5}
          onClick={() => console.log('click')}
          onMouseover={(props) => console.log(props.center)}
          fillColor={'#'+radHue['hue']}
          fillOpacity={0.6}/>)
      })
      const listResult = Object.keys(actualObj).map((value, index, array)=>{
        const predictionError = (Math.abs(actualObj[value]+1 - (predictObj[value]+1)))/(actualObj[value]+1)
        const radHue = pred_rad_and_hue(predictionError)
        return {"state":value, "prediction": predictObj[value], "actual" : actualObj[value], "rad":radHue['rad'], "hue":radHue['hue']}
      })
      setMapArray(circleResult)
      setListArray(listResult)
   }
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
                containerStyle = {{left: '2%', right:0, top: '27%', position: 'absolute', width:'70%', height : '72%'}}
                initialCenter={
                  {
                    lat:39.8097343, 
                    lng: -98.5556199
                  }
                }>
                  {mapArray}
              </Map>
              <Slider
                className = {classes.slider}
                defaultValue={(actualkeys.length - 1) * 7
                }
                valueLabelFormat = {value => nextDay(actualStartDate , value)}
                aria-labelledby="discrete-slider"
                valueLabelDisplay="auto"
                step={7}
                marks
                onChange = {handleChange}
                min={0}
                max={(actualkeys.length - 1) * 7}
              />
            </div>
            <div id="space"></div>
            <div id="list">
              <h4 style={{marginBottom: '1rem', fontSize: '30px'}}>Prediction vs History</h4>
              <List  className = {classes.root}>
                {listArray.map(({state, prediction, actual, rad , hue})=>(
                  <ListItem key ={state}>
                    <ListItemText primary={state + ": " + prediction + " vs " + actual }/>
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
