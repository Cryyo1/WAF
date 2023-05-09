import React,{useEffect} from 'react';
import { useSearchParams } from 'react-router-dom';
import axios from 'axios';

const DetailedReq = () => {
    const [HttpRequets,setHttpRequests] = React.useState(null);
    useEffect(() => {
        axios.get('http://localhost:5000/requests')
            .then(res => {
                console.log(res.data);
                setHttpRequests(res.data)
            }).catch(err => {
                console.log(err);
            });
    }, []);
    const [searchParams] = useSearchParams();
    const getRequest = () => {
        console.log(searchParams.entries());
        let request = HttpRequets[searchParams.get("id")];
        if (request === undefined) {
            return (
                <div className="flex flex-row p-10">
                    <h1 className='font-semibold'>No Request Found</h1>
                </div>
            )
        }
        console.log(request);
        const render = Object.keys(request).map((key) => {
            if(key !== "Headers" && key !== "Data"){
                return(
                <div className="flex flex-row items-center space-x-2">
                    <h1 className='font-semibold'>{key} : </h1> <p>{request[key]}</p>
                </div>)
            }else{
                return ''
            }
        })
        let Headers = request["Headers"];
        const renderHeaders = Object.keys(Headers).map((key) => {
            return(
                <div className="flex flex-row items-center space-x-2">
                    <h1 className='font-semibold'>{key} : </h1> <p>{Headers[key]}</p>
                </div>)
        })
        let Data = (
            <div className="flex flex-row items-center space-x-2">
                <h1 className='font-bold font-lg text-red-600'>{`\n \n ${request["Data"]}`} </h1> 
            </div>)
        return [render , renderHeaders , Data];
        
    }
    if (!HttpRequets) {
        return <div className='text-grey-color'>Loading...</div>;
    }


    return (
        <div className="h-screen flex items-left rounded-md flex-col">
            {getRequest()}
        </div>
    );
}
export default DetailedReq;