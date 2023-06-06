import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';

const Requests = (props) => {
    // define states
    // httpRequests: list of http requests
    const [HttpRequets,setHttpRequests] = React.useState(null);
    // use effect to get the http requests
    useEffect(() => {
        axios.get('http://localhost:5000/requests')
            .then(res => {
                setHttpRequests(res.data)
                console.log("data updated!!")
            }).catch(err => {
                console.log(err);
            });
        const intervall=setInterval(()=>{
            axios.get('http://localhost:5000/requests')
            .then(res => {
                setHttpRequests(res.data)
                console.log("data updated!!")
            }).catch(err => {
                console.log(err);
            });    
        },10000)
        return () => clearInterval(intervall)
    }, []);
    // code to navigate to the request page
    const navigate = useNavigate();
    const goToReq = (id) => {
        navigate({
            pathname: '/request',
            search: `?id=${id}`,
        });
    }
    // transform the http requests to jsx code  headers
    const Headers = () => {
        let columns = ["Date time","Method","Path","Class","Type","Action"]
        const cols = columns.map((column, index) => {
            if (index === 0) {
                return <th key={index} className="p-3 rounded-l-md">{column}</th>
            } else if (index === columns.length - 1) {
                return <th key={index} className="p-3 rounded-r-md">{column}</th>
            } else {
                return <th key={index} className="p-3 ">{column}</th>
            }
        });
        return [cols];
    }
    // transform the http requests to jsx code  rows
    const Rows = () => {
        // filter the http requests by the filter selected by the user either all, normal or abnormal or the method or the type
        const HttpRequetsFiltered = HttpRequets.filter((elem) => elem.Type === props.filter || elem.Class == props.filter  || elem.Method == props.filter|| props.filter === 'all')
        const rows = HttpRequetsFiltered.map((row, index) => {
            return (
                <tr key={index} className="bg-white text-grey-color space-y-5 rounded-md h-full">
                    <td className="p-3 rounded-l-md">{row["Date time"]}</td>
                    <td className="p-3 rounded-l-md">{row.Method}</td>
                    <td className="p-3 ">{row.Path}</td>
                    <td className="p-3 ">
                        {(row.Class === 'Anormale') ? <div className="bg-red-500 rounded-md text-sm p-1 m-2 text-white text-center">{row.Class}</div> : <div className="bg-green-500 rounded-md text-sm p-1 m-2 text-white text-center">{row.Class}</div>}
                    </td>
                    <td className="p-3 ">{(row.Type !== '') ? <div className="bg-red-500 rounded-md text-sm p-1 m-2 text-white text-center">{row.Type}</div> : <div></div>}</td>
                    <td className="p-3 rounded-r-md"><button onClick={() => goToReq(row.Id)} className="text-sm text-white bg-primary rounded-md p-1 m-2 hover:bg-[#e2c389] ...">Afficher</button></td>
                </tr>
            );
        });
        return [rows];
    }
    // jsx code if the http requests are not loaded yet 
    if (!HttpRequets) {
        return <div className='text-grey-color'>Loading...</div>;
    }
    // jsx code if the http requests are loaded
    return (
        <div className="flex justify-center h-fit max-h-full">
                <table className="table text-gray-400 border-separate border-spacing-y-1 text-sm mt-0 pt-0">
                    <thead className="bg-white text-grey-color">
                        <tr className="bg-white text-grey-color rounded-md">
                            <Headers />
                        </tr>
                    </thead>

                    <tbody className="">
                        <Rows />
                    </tbody>

                </table>
        </div >
        
    );
}

export default Requests;