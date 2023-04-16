import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';

const Requests = () => {
    const [HttpRequets,setHttpRequests] = React.useState(null);
    useEffect(() => {
        axios.get('http://localhost:5000/requests')
            .then(res => {
                setHttpRequests(res.data)
            }).catch(err => {
                console.log(err);
            });
    }, []);
    const navigate = useNavigate();
    const goToReq = (id) => {
        navigate({
            pathname: '/request',
            search: `?id=${id}`,
        });
    }

    const Headers = () => {
        let columns = Object.keys(HttpRequets[0]).filter((key) => (key !== "Data" && key !== "Headers"));
        columns.push("Action")
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
    const Rows = () => {
        const rows = HttpRequets.map((row, index) => {
            return (
                <tr key={index} className="bg-white text-grey-color space-y-5 rounded-md h-full">
                    <td className="p-3 rounded-l-md">{row.Method}</td>
                    <td className="p-3 ">{row.Path}</td>
                    <td className="p-3 ">
                        {(row.Class === 'anormale') ? <div className="bg-red-500 rounded-md text-sm p-1 m-2 text-white text-center">{row.Class}</div> : <div className="bg-green-500 rounded-md text-sm p-1 m-2 text-white text-center">{row.Class}</div>}
                    </td>
                    <td className="p-3 ">{(row.Type !== '') ? <div className="bg-red-500 rounded-md text-sm p-1 m-2 text-white">{row.Type}</div> : <div></div>}</td>
                    <td className="p-3 rounded-r-md"><button onClick={() => goToReq(index)} className="text-sm text-white bg-primary rounded-md p-1 m-2 hover:bg-[#e2c389] ...">More ...</button></td>
                </tr>
            );
        });
        return [rows];
    }
    if (!HttpRequets) {
        return <div className='text-grey-color'>Loading...</div>;
    }
    return (

        <div className="flex justify-center">
            <div className="overflow-x-scroll  lg:overflow-visible">
                <table className="table text-gray-400 border-separate border-spacing-y-1 text-sm">
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
        </div>
    );
}

export default Requests;