import React from 'react';

const Informations = (props) => {
    return (
        <div className="flex flex-col items-left text-grey-color bg-white p-5 space-y-2 rounded-md ">
            <div className="flex flex-row items-center space-x-2">
                <h1 className='font-semibold'>Nombre des requetes http totals : </h1> <p>{props.requests}</p>
            </div>

            <div className="flex flex-row items-center space-x-2">
                <h1 className='font-semibold'>Nombre des requetes http Bloquées : </h1> <p>{props.blocked}</p>
            </div>

            <div className="flex flex-row items-center space-x-2">
                <h1 className='font-semibold'>Nombre des requetes http Acceptées : </h1> <p>{props.accepted}</p>
            </div>

            <div className="flex flex-row items-center space-x-2">
                <h1 className='font-semibold'>Statue du serveur proxy inversé : </h1> {(props.status === "Up" ? <p className="text-green-500">Up</p> : <p className="text-red-500">Down</p>)}
            </div>

            <div className="flex flex-row items-center space-x-2">
                <h1 className='font-semibold'>Adresse IP du serveur : </h1> <p>{props.ip}</p>
            </div>

            <div className="flex flex-row items-center space-x-2">
                <h1 className='font-semibold'>Port du serveur : </h1> <p>{props.port}</p>
            </div>


        </div>
    )
}

export default Informations;