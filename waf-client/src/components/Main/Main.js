import React,{ useEffect } from 'react';
import Graph from './Graph';
import Requests from './Requests';
import Informations from './Informations';
import axios from 'axios';
import NavBar from '../Navbar/Navbar';

const Main = (props) => {
    const [HttpRequets,setHttpRequests] = React.useState(null);
    const [name,setName]=React.useState('')
    const [email,setEmail]=React.useState('')
    useEffect(() => {
        axios.get('http://localhost:5000/requests')
            .then(res => {
                setHttpRequests(res.data)
            }).catch(err => {
                console.log(err);
            });
        axios.get('http://localhost:5000/user')
        .then(res => {
            setEmail(res.data.email)
            setName(res.data.name)
        }).catch(err => {
            console.log(err);
        });
    }, []);



    if (!HttpRequets) {
        return <div className='text-grey-color'>Loading...</div>;
    }
    return (
        <>
        <NavBar name={name} email={email} />
        <div className="grid grid-cols-2 gap-4  grid-rows-2 h-screen max-h-full m-8">
            <div className="col-span-1 row-span-1 w-full h-full bg-white rounded-md pl-2"> <Graph /></div>
            <div className="col-span-1 row-span-2 w-full h-full overflow-y:scroll mt-0"><Requests /></div>
            <div className="col-span-1 row-span-1 w-full h-full rounded-md ">
                <Informations requests={HttpRequets.length}
                    ip="127.0.0.1"
                    port="8080"
                    blocked={HttpRequets.filter((elem) => elem.Class === "anormale").length}
                    accepted={HttpRequets.filter((elem) => elem.Class === "normale").length}
                    status="Down" />
            </div>

        </div>
        </>
        
    );
}

export default Main;