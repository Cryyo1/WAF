import React from 'react';
import logo from '../../assets/sonatrach-logo-vector.svg';
import { Context } from "../../store/appContext";
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const { store , actions } = React.useContext(Context);
  const navigate= useNavigate();

  const handleLogin = () => {
    console.log(store.token);
    actions.login(email, password).then(() => {
      navigate({
        pathname:"/home"
      });
    });
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault(); // prevent default form submit
      handleLogin();
    }
  }

  if(store.token && store.token !== '' && store.token !== undefined) {
    navigate({
      pathname:"/home"
    });
  }

  return (
    <div className="h-screen flex items-center justify-center rounded-md" tabIndex="0">
      <div className="flex flex-col justify-center items-center space-y-4 w-1/2 p-10 bg-white" tabIndex="0">
        <img src={logo} alt="sonatrach logo" className="h-1/5 w-1/5 m-6" />
        <h1 className="font-semibold text-lg text-grey-color">Waf-IA</h1>
        <input type="email" placeholder="Email" className="border rounded-md border-grey-color p-2 focus:ring-primary
          focus:outline-none
          focus:border-primary
          focus:placeholder-transparent"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input type="password" placeholder="Password" className="border rounded-md border-grey-color p-2 focus:ring-primary
          focus:outline-none
          focus:border-primary
          focus:placeholder-transparent"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit"
          className="text-white bg-primary p-2 w-1/4 rounded-md border border-grey-100 hover:text-primary hover:bg-white hover:border-primary"
          onClick={handleLogin}
          onKeyPress={handleKeyPress}
          tabIndex="0">
          Login
        </button>
      </div>
    </div>
  );
}

export default Login;
