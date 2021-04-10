import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <div id="header">
        <h4>Number of Hate Crimes againt Racial Minorities in U.S. by States</h4>
        <p id="description">
          short description goes here !!
        </p>
      </div>
      <div id="app-container">
        <table>
          <tr>
            <td id="map">
              map comes here!
            </td>
            <td id="space"></td>
            <td id="list">
              list in descending order here!
            </td>
          </tr>
        </table>
      </div>
    </div>
  );
}

export default App;
