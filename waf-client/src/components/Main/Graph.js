import  react, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import Chart from 'chart.js/auto';


const Graph = () => {
  const [chartData, setChartData] = useState(null);
  const [showRequests, setShowRequests] = useState(true);
  const [showSQLi, setShowSQLi] = useState(true);
  const [showXSS, setShowXSS] = useState(true);
  const [showCMDi, setShowCMDi] = useState(true);
  const [showPTR, setShowPTR] = useState(true);

  useEffect(() => {
    const fetchData = () => {
      axios
        .get('http://localhost:5000/data')
        .then(res => {
          const chartData = {
            labels: res.data.map(elem => elem.date),
            datasets: [
              showRequests && {
                label: "Total",
                data: res.data.map(elem => elem.requests),
                borderColor: '#ff8500',
                backgroundColor: 'rgba(255, 133, 0, 0.2)',
              },
              showSQLi && {
                label: "SQL injection",
                data: res.data.map(elem => elem.sqli),
                borderColor: '#607EAA',
                backgroundColor: 'rgba(96, 126, 170, 0.2)', // lighter version of borderColor
              },
              showXSS && {
                label: "Cross-Site-Scripting",
                data: res.data.map(elem => elem.xss),
                borderColor: '#EBC7E8',
                backgroundColor: 'rgba(235, 199, 232, 0.2)', // lighter version of borderColor
              },
              showCMDi && {
                label: "Command Injection",
                data: res.data.map(elem => elem.cmdi),
                borderColor: '#F24C4C',
                backgroundColor: 'rgba(242, 76, 76, 0.2)', // lighter version of borderColor
              },
              showPTR && {
                label: "Path Traversal",
                data: res.data.map(elem => elem.ptr),
                borderColor: '#76BA99',
                backgroundColor: 'rgba(118, 186, 153, 0.2)', // lighter version of borderColor
              }
              
            ].filter(Boolean),
          };
          setChartData(chartData);
        })
        .catch(err => {
          console.log(err);
        });
    };

    fetchData();

    const interval = setInterval(fetchData, 10000);

    return () => clearInterval(interval);
  }, [showRequests, showSQLi, showXSS, showCMDi, showPTR]);

  if (!chartData) {
    return <div className='text-grey-color'>Loading...</div>;
  }

  return (
    <div className="rounded-md">
      <Line
        data={chartData}
        options={{
          plugins: {
            title: {
              display: true,
              text: "Nombre des requêtes bloquées les 7 derniers jours"
            },
            legend: {
              display: true
            }
          }
        }}
        className="mt-4"
      />
      <div className='flex flex-row space-x-4 justify-center m-3'>

        <ul class="flex flex-row">
          <li class="w-full">
            <div class="flex items-center pl-3">
              <input id="sqli-checkbox-list" type="checkbox" value="" class="w-4 h-4 text-white accent-primary border-grey-color rounded focus:ring-primary focus:ring-1"
                checked={showSQLi} onChange={e => setShowSQLi(e.target.checked)} />
              <label for="sqli-checkbox-list" class="w-full py-3 ml-2 text-sm font-medium  text-grey-color  ">SQLi</label>
            </div>
          </li>
          <li class="w-full">
            <div class="flex items-center pl-3">
              <input id=" xss-checkbox-list" type="checkbox" value="" class="w-4 h-4 text-white accent-primary border-grey-color rounded focus:ring-primary focus:ring-1"
                checked={showXSS} onChange={e => setShowXSS(e.target.checked)} />
              <label for=" xss-checkbox-list" class="w-full py-3 ml-2 text-sm font-medium  text-grey-color">XSS</label>
            </div>
          </li>
          <li class="w-full">
            <div class="flex items-center pl-3">
              <input id=" ptr-checkbox-list" type="checkbox" value="" class="w-4 h-4 text-white accent-primary  border-grey-color rounded focus:ring-primary focus:ring-1"
                checked={showPTR} onChange={e => setShowPTR(e.target.checked)} />
              <label for=" ptr-checkbox-list" class="w-full py-3 ml-2 text-sm font-medium  text-grey-color">PTR</label>
            </div>
          </li>
          <li class="w-full">
            <div class="flex items-center pl-3">
              <input id=" cmdi-checkbox-list" type="checkbox" value="" class="w-4 h-4 text-white accent-primary border-grey-color rounded focus:ring-primary focus:ring-1 "
                checked={showCMDi} onChange={e => setShowCMDi(e.target.checked)} />
              <label for=" cmdi-checkbox-list" class="w-full py-3 ml-2 text-sm font-medium  text-grey-color  ">CMDi</label>
            </div>
          </li>
        </ul>
      </div>

    </div>
  );
};

export default Graph;
