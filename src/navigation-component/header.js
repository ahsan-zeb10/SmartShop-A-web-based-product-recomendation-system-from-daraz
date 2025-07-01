import React from 'react';
import { NavLink } from 'react-router-dom';
import { useUndoRedo } from '../context/UndoRedoContext';
import logo from './logo.png'

const Header = () => {
  const { undo, redo } = useUndoRedo();

  return (
    <header>
      <nav className="bg-white border-gray-200 px-4 lg:px-6 py-2.5">
        <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
          <div className="flex items-center space-x-4">
            <button
              onClick={undo}
              className="p-2 rounded-full hover:bg-gray-100 transition-colors duration-200"
              title="Undo"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              onClick={redo}
              className="p-2 rounded-full hover:bg-gray-100 transition-colors duration-200"
              title="Redo"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
            <NavLink to="/" className="flex items-center">
            <img
              src={logo}
              className="mr-3 h-10 sm:h-20"
                alt="SmartShop Logo"
            />
            <span className="self-center text-xl font-semibold whitespace-nowrap">
                SmartShop
            </span>
            </NavLink>
          </div>
          <div className="flex items-center lg:order-2">
            {/* <NavLink
              to="/login"
              className="text-gray-800 hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 focus:outline-none"
            >
              Log in
            </NavLink> */}
            {/* <NavLink
              to="/signup"
              className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 focus:outline-none"
            >
              Get started
            </NavLink> */}
            <button
              data-collapse-toggle="mobile-menu-2"
              type="button"
              className="inline-flex items-center p-2 ml-1 text-sm text-gray-500 rounded-lg lg:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200"
              aria-controls="mobile-menu-2"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              <svg
                className="w-6 h-6"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fillRule="evenodd"
                  d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                  clipRule="evenodd"
                ></path>
              </svg>
              <svg
                className="hidden w-6 h-6"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                ></path>
              </svg>
            </button>
          </div>
          <div
            className="hidden justify-between items-center w-full lg:flex lg:w-auto lg:order-1"
            id="mobile-menu-2"
          >
            <ul className="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-8 lg:mt-0">
              <li>
                <NavLink
                  to="/"
                  className={({ isActive }) => 
                    `block py-2 pr-4 pl-3 rounded lg:bg-transparent lg:p-0 ${
                      isActive 
                        ? 'text-blue-700' 
                        : 'text-gray-700 hover:bg-gray-50 lg:hover:bg-transparent lg:hover:text-blue-700 lg:border-0'
                    }`
                  }
                >
                  Home
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/marketplace"
                  className={({ isActive }) => 
                    `block py-2 pr-4 pl-3 rounded lg:bg-transparent lg:p-0 ${
                      isActive 
                        ? 'text-blue-700' 
                        : 'text-gray-700 hover:bg-gray-50 lg:hover:bg-transparent lg:hover:text-blue-700 lg:border-0'
                    }`
                  }
                >
                  Marketplace
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/about"
                  className={({ isActive }) => 
                    `block py-2 pr-4 pl-3 rounded lg:bg-transparent lg:p-0 ${
                      isActive 
                        ? 'text-blue-700' 
                        : 'text-gray-700 hover:bg-gray-50 lg:hover:bg-transparent lg:hover:text-blue-700 lg:border-0'
                    }`
                  }
                >
                  About
                </NavLink>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;
