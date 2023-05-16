import React, { useEffect } from 'react';
import axios from 'axios';

const Informations = (props) => {
    const [status, setStatus] = React.useState(null);
    useEffect(() => {
        axios.get('http://localhost:5000/status')
            .then(res => {
                console.log(res.data)
                setStatus(res.data)
            }).catch(err => {
                console.log(err);
            });
        const intervall = setInterval(() => {
            axios.get('http://localhost:5000/status')
                .then(res => {
                    setStatus(res.data)
                }).catch(err => {
                    console.log(err);
                });
        }, 10000)
        return () => clearInterval(intervall)
    }, []);

    if (!status) {
        return <div className='text-grey-color'>Loading...</div>;
    }
    return (
        <div className="flex flex-col items-left text-grey-color bg-white p-5 space-y-2 rounded-md ">
            <div>
                <h1 className='font-semibold text-primary'>Statistiques : </h1>
                <div className="flex flex-row items-center space-x-2">
                    <h1 className='font-semibold'>Nombre des requetes http totals : </h1> <p>{props.requests}</p>
                </div>

                <div className="flex flex-row items-center space-x-2">
                    <h1 className='font-semibold'>Nombre des requetes http Bloquées : </h1> <p>{props.blocked}</p>
                </div>

                <div className="flex flex-row items-center space-x-2">
                    <h1 className='font-semibold'>Nombre des requetes http Acceptées : </h1> <p>{props.accepted}</p>
                </div>
            </div>

            <div>
                <h1 className='font-semibold text-primary'>Configuration : </h1>
                <div className="flex flex-row items-center space-x-2">
                    <h1 className='font-semibold'>Statue du serveur proxy inversé : </h1> {(status.status === "Up" ? <p className="text-green-500">Up</p> : <p className="text-red-500">Down</p>)}
                </div>

                <div className="flex flex-row items-center space-x-2">
                    <h1 className='font-semibold'>Adresse IP du serveur : </h1> <p>{status.ip}</p>
                </div>

                <div className="flex flex-row items-center space-x-2">
                    <h1 className='font-semibold'>Port du serveur : </h1> <p>{status.port}</p>
                </div>
            </div>



        </div>
    )
}

export default Informations;