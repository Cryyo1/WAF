import React, { useState, useEffect } from 'react';
import logo from '../../assets/sonatrach-logo-vector.svg';
import { Context } from "../../store/appContext";

const NavBar = (props) => {
  // define states
  // keyword: search keyword
  // showMenu: show or hide the menu
  // actions: login and logout actions from the store
  const [keyword, setKeyword] = useState('');
  const [showMenu, setShowMenu] = useState(false);
  const { actions } = React.useContext(Context);
  const handleLogout = () => {
    actions.logout()
  }
  // use effect to handle click outside the menu
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showMenu && !event.target.closest('#avatarButtonMenu')) {
        setShowMenu(false);
      }
    }
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    }
  }, [showMenu]);


  // jsx code for the navbar (logo, search bar, profile picture)
  return (
    <div className="relative flex flex-row h-16 m-8 rounded-md justify-start items-center bg-white text-grey-color">
      <img src={logo} alt="sonatrach logo" className="h-4/5 m-6" />
      <h1 className="font-semibold font-base mr-6">WAF-IA</h1>
      <input
        type="text"
        className="
          h-1/2
          w-1/2
          text-sm
          font-normal
          m-6
          p-4
          pl-8
          rounded-md
          border-grey-color
          text-grey-color
          bg-white
          border
          border-solid
          
          placeholder-grey-color
          placeholder:text-center 
          focus:ring-primary
          focus:outline-none
          focus:border-primary
          focus:placeholder-transparent
        "
        id="search"
        name="search"
        placeholder="Recherche..."
        onChange={(e) => {
          setKeyword(e.target.value)
          props.changeFilter(e.target.value)
        }
        }
      />
      <div className="flex flex-col ml-36 mr-6">
        <h1 className='font-medium text-grey'>{props.name}</h1>
        <h1 className='font-regular text-sm text-grey ml-2'>{props.email}</h1>
      </div>
      <div className="relative">
        <img
          src={process.env.PUBLIC_URL + '/profiles/'+ props.profilePicture}
          className="h-10 w-10 rounded-full cursor-pointer"
          id="avatarButtonMenu"
          alt="profile"
          onClick={() => setShowMenu(!showMenu)}
        />
        {showMenu &&
          <div className="absolute top-14 right-0 z-10 bg-white border border-gray-200 rounded-md shadow-md" id="avatarButtonMenu">
            <button className="block w-full text-left px-4 py-2 hover:bg-gray-100" onClick={handleLogout}>Logout</button>
          </div>
        }
      </div>
    </div>
  );
};

export default NavBar;
