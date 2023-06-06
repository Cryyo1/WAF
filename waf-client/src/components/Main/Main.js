import React, { useEffect } from 'react';
import Graph from './Graph';
import Requests from './Requests';
import Informations from './Informations';
import axios from 'axios';
import NavBar from '../Navbar/Navbar';
import "./style.css";

const Main = (props) => {
  // define states
  // httpRequests: list of http requests
  // name: user name
  // email: user email
  // filter: filter for the requests
  const [httpRequests, setHttpRequests] = React.useState(null);
  const [name, setName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [profilePicture, setProfilePicture] = React.useState('');
  const [filter, setFilter] = React.useState('all');
  // use effect to get the http requests and the user info
  useEffect(() => {
    axios.get('http://localhost:5000/requests')
      .then(res => {
        setHttpRequests(res.data);
      })
      .catch(err => {
        console.log(err);
      });
    axios.get('http://localhost:5000/user')
      .then(res => {
        setEmail(res.data.email);
        setName(res.data.name);
        setProfilePicture(res.data.profilePicture);
      })
      .catch(err => {
        console.log(err);
      });
  }, []);
  // function to change the filter
  const changeFilter = (filter) => {
    if (filter === '') {
      setFilter('all');
    }else{
      setFilter(filter);
    }
    
  }
  // jsx code for the main page if the http requests are not loaded yet
  if (!httpRequests) {
    return <div className='text-grey-color'>Loading...</div>;
  }
  // jsx code for the main page if the http requests are loaded (navbar, graph, requests, informations)
  return (
    <div className="h-screen scrollbar-hide">
      <NavBar name={name} email={email} profilePicture={profilePicture} changeFilter={changeFilter} />
      <div className="grid grid-cols-5 gap-4 grid-rows-2 h-full max-h-full m-8 scroll-hide">
        <div className="col-span-2 row-span-1 w-full h-full bg-white rounded-md pl-2 m-0">
          <Graph />
        </div>
        <div className="col-span-3 row-span-2 w-full h-full mt-0 overflow-auto scroll-hide">
          <Requests filter={filter}/>
        </div>
        <div className="col-span-2 row-span-1 w-full h-screen rounded-md">
          <Informations
            requests={httpRequests.length}
            blocked={httpRequests.filter((elem) => elem.Class === "Anormale").length}
            accepted={httpRequests.filter((elem) => elem.Class === "Normale").length}
          />
        </div>
      </div>
    </div>
  );
}

export default Main;
