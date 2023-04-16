const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token:null,
			message: null,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			]
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},
			syncTokenFromSessionStore:()=>{
				const access_token=sessionStorage.getItem("access_token")
				if (access_token && access_token !== '' && access_token !== undefined){
					console.log(access_token)
					setStore({token:access_token})
				}
			},
			isAuthenticated: () =>{
				const token=sessionStorage.getItem("access_token")
				if( !token || token === '' || token ===  undefined)
					return false
				return true
 
			},
			logout:()=>{
				sessionStorage.removeItem("access_token")
				setStore({token:null})
			},
			login: async (email,password) => {
				const data = {
					email: email,
					password: password
				}
				const resp=await fetch('http://127.0.0.1:5000/api/login', {
					method: 'POST',
					body: JSON.stringify(data),
					headers: {
						'Content-Type': 'application/json'
					}
				})
				if (resp.status !== 200){
					console.log("login failed !!")
					return false
				}
				try{
					const respData= await resp.json();
					sessionStorage.setItem("access_token",respData["access_token"])
					setStore({token:data.access_token})
					return true
				}catch(err){
					console.log(err)
				}

			},
			getMessage: async () => {
				try{
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				}catch(error){
					console.log("Error loading message from backend", error)
				}
			},
			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			}
		}
	};
};

export default getState;