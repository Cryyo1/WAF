import React, { useEffect } from 'react';
import Graph from './Graph';
import Requests from './Requests';
import Informations from './Informations';
import axios from 'axios';
import NavBar from '../Navbar/Navbar';
import "./style.css";

const Main = (props) => {
  const [httpRequests, setHttpRequests] = React.useState(null);
  const [name, setName] = React.useState('');
  const [email, setEmail] = React.useState('');
  
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
      })
      .catch(err => {
        console.log(err);
      });
  }, []);

  if (!httpRequests) {
    return <div className='text-grey-color'>Loading...</div>;
  }

  return (
    <div className="h-screen scrollbar-hide">
      <NavBar name={name} email={email} />
      <div className="grid grid-cols-5 gap-4 grid-rows-2 h-full max-h-full m-8 scroll-hide">
        <div className="col-span-2 row-span-1 w-full h-full bg-white rounded-md pl-2 m-0">
          <Graph />
        </div>
        <div className="col-span-3 row-span-2 w-full h-full mt-0 overflow-auto scroll-hide">
          <Requests />
        </div>
        <div className="col-span-2 row-span-1 w-full h-screen rounded-md">
          <Informations
            requests={httpRequests.length}
            blocked={httpRequests.filter((elem) => elem.Class === "anormale").length}
            accepted={httpRequests.filter((elem) => elem.Class === "normale").length}
          />
        </div>
      </div>
    </div>
  );
}

export default Main;
