import { Route, Routes } from "react-router-dom";
import { useState } from "react";
import Header from "./navigation-component/header";
import Home from "./home/home";
import Marketplace from "./marketplace/marketplace";
import About from "./about/about";
import CategoryProducts from './marketplace/CategoryProducts';
import { UndoRedoProvider } from "./context/UndoRedoContext";

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = (query) => {
    setSearchQuery(query);
    setIsSearching(true);
    // Simulate API call or add your actual search logic here
    setTimeout(() => {
      setSearchResults([/* your search results */]);
      setIsSearching(false);
    }, 1000);
  };

  return (
    <UndoRedoProvider>
    <div>
        <Header 
          searchQuery={searchQuery}
          onSearch={handleSearch}
        />
      <Routes>
          <Route 
            path="/" 
            element={
              <Home 
                searchQuery={searchQuery}
                isSearching={isSearching}
                searchResults={searchResults}
                onSearch={handleSearch}
              />
            } 
          />
          <Route path="/marketplace" element={<Marketplace />} />
          <Route path="/marketplace/:category" element={<CategoryProducts />} />
          <Route path="/about" element={<About />} />
      </Routes>
    </div>
    </UndoRedoProvider>
  );
}

export default App;
