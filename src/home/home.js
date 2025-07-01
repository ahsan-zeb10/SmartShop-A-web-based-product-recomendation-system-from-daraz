// import React from "react";
// import { useUndoRedo } from "../context/UndoRedoContext";
// import ProductList from "./productlist";
// import SearchBar from "./searchbar";

// const Home = () => {
//   const { state, setState } = useUndoRedo();

//   const handleSearch = (query) => {
//     const newState = {
//       searchQuery: query,
//       isSearching: true,
//       searchResults: []
//     };
//     setState(newState);
    
//     // Simulate API call
//     setTimeout(() => {
//       const updatedState = {
//         ...newState,
//         isSearching: false,
//         searchResults: []
//       };
//       setState(updatedState);
//     }, 1000);
//   };

//   return (
//     <div className="flex flex-col items-center min-h-screen bg-gradient-to-b from-white to-sky-300">
//       {}
//       {!state.present?.searchQuery && (
//         <div className="text-center mb-4 mt-20">
//           <h1 className="text-3xl font-bold text-gray-800">
//             Find The Best Product With Our Recommendations
//           </h1>
//           <p className="mt-4 text-gray-600 text-2xl">Smart shopping made simple</p>
//         </div>
//       )}

//       {/* Search Bar */}
//       <div
//         className={`w-full px-4 transition-all duration-500 mt-20 ${
//           state.present?.searchQuery ? "mt-4" : "mt-20"
//         }`}
//       >
//         <SearchBar 
//           onSearch={handleSearch} 
//           initialValue={state.present?.searchQuery || ""} 
//         />
//       </div>

//       {/* Product List */}
//       {state.present?.searchQuery && (
//         <div className="w-full mt-6 px-4">
//           {state.present?.isSearching ? (
//             <div className="flex justify-center items-center py-8">
//               <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
//               <span className="ml-4 text-gray-600">Searching for products...</span>
//             </div>
//           ) : (
//             <ProductList 
//               searchTerm={state.present?.searchQuery} 
//               results={state.present?.searchResults} 
//             />
//           )}
//         </div>
//       )}
//     </div>
//   );
// };

// export default Home;






// import React, { useState, useEffect } from "react";
// import { useUndoRedo } from "../context/UndoRedoContext";
// import ProductList from "./productlist";
// import SearchBar from "./searchbar";

// const Home = () => {
//   const { state, setState } = useUndoRedo();
//   const [loading, setLoading] = useState(false);
//   const [searchResults, setSearchResults] = useState([]);
//   const [recommendations, setRecommendations] = useState([]);

//   // Function to fetch products from API based on search query
//   const fetchProducts = async (query) => {
//     setLoading(true);
//     try {
//       const response = await fetch(`http://localhost:8000/api/search?query=${query}`);
//       const data = await response.json();

//       if (data.success) {
//         setSearchResults(data.data); // Update searchResults with API data
//       } else {
//         throw new Error("Failed to fetch products.");
//       }
//     } catch (error) {
//       console.error("Error fetching products:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Function to handle search
//   const handleSearch = (query) => {
//     setState({
//       searchQuery: query,
//       isSearching: true,
//       searchResults: [],
//     });
//     fetchProducts(query); // Call the fetchProducts function on search
//   };

//   // Function to generate recommendations based on previous product clicks stored in localStorage
//   useEffect(() => {
//     const clickedProducts = JSON.parse(localStorage.getItem("clickedProducts")) || [];
//     const recommendedProducts = generateRecommendations(clickedProducts);
//     setRecommendations(recommendedProducts);
//   }, [searchResults]); // Recalculate recommendations based on new search results

//   const generateRecommendations = (clickedProducts) => {
//     const allProducts = searchResults || [];
//     let recommended = allProducts.filter((product) => {
//       return clickedProducts.some(
//         (id) => product.category === allProducts.find((p) => p.id === id)?.category
//       );
//     });
//     return recommended;
//   };

//   // Function to track product clicks and save them in localStorage
//   const trackProductClick = (productId) => {
//     let clickedProducts = JSON.parse(localStorage.getItem("clickedProducts")) || [];
//     if (!clickedProducts.includes(productId)) {
//       clickedProducts.push(productId);
//     }
//     localStorage.setItem("clickedProducts", JSON.stringify(clickedProducts));
//   };

//   return (
//     <div className="flex flex-col items-center min-h-screen bg-gradient-to-b from-white to-sky-300">
//       {!state.present?.searchQuery && (
//         <div className="text-center mb-4 mt-20">
//           <h1 className="text-3xl font-bold text-gray-800">
//             Find The Best Product With Our Recommendations
//           </h1>
//           <p className="mt-4 text-gray-600 text-2xl">Smart shopping made simple</p>
//         </div>
//       )}

//       {/* Search Bar */}
//       <div
//         className={`w-full px-4 transition-all duration-500 mt-20 ${
//           state.present?.searchQuery ? "mt-4" : "mt-20"
//         }`}
//       >
//         <SearchBar onSearch={handleSearch} initialValue={state.present?.searchQuery || ""} />
//       </div>

//       {/* Recommendations */}
//       {recommendations.length > 0 && (
//         <div className="w-full mt-6 px-4">
//           <h2 className="text-2xl font-bold text-center">Recommended for You</h2>
//           <div className="flex justify-center mt-4">
//             {recommendations.map((product) => (
//               <div
//                 key={product.id}
//                 onClick={() => trackProductClick(product.id)}
//                 className="cursor-pointer p-4 border rounded-lg m-2 hover:shadow-lg"
//               >
//                 <img src={product.image_url} alt={product.title} className="w-full h-40 object-contain mb-4" />
//                 <h3 className="text-md font-semibold">{product.title}</h3>
//                 <p className="text-gray-700 font-bold">Rs {product.price}</p>
//               </div>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Product List */}
//       {state.present?.searchQuery && (
//         <div className="w-full mt-6 px-4">
//           {loading ? (
//             <div className="flex justify-center items-center py-8">
//               <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
//               <span className="ml-4 text-gray-600">Searching for products...</span>
//             </div>
//           ) : (
//             <ProductList
//               searchTerm={state.present?.searchQuery}
//               results={searchResults} // Pass results from the search API to ProductList
//               onProductClick={trackProductClick} // Track product click
//             />
//           )}
//         </div>
//       )}
//     </div>
//   );
// };

// export default Home;



// import React, { useState, useEffect, useCallback } from "react";
// import { useUndoRedo } from "../context/UndoRedoContext";
// import ProductList from "./productlist";
// import SearchBar from "./searchbar";

// const Home = () => {
//   const { state, setState } = useUndoRedo();
//   const [loading, setLoading] = useState(false);
//   const [searchResults, setSearchResults] = useState([]);
//   const [recommendations, setRecommendations] = useState([]);

//   // Function to fetch products from API based on search query
//   const fetchProducts = async (query) => {
//     setLoading(true);
//     try {
//       const response = await fetch(`http://localhost:8000/api/search?query=${query}`);
//       const data = await response.json();

//       if (data.success) {
//         setSearchResults(data.data); // Update searchResults with API data
//       } else {
//         throw new Error("Failed to fetch products.");
//       }
//     } catch (error) {
//       console.error("Error fetching products:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Function to handle search
//   const handleSearch = (query) => {
//     setState({
//       searchQuery: query,
//       isSearching: true,
//       searchResults: [],
//     });
//     fetchProducts(query); // Call the fetchProducts function on search
//   };

//   // Memoized function to generate recommendations
//   const generateRecommendations = useCallback((clickedProducts, searchHistory) => {
//     let recommended = [];
    
//     // If clickedProducts have data, fetch recommendations based on categories
//     if (clickedProducts.length > 0) {
//       recommended = searchResults.filter((product) => {
//         return clickedProducts.some(
//           (id) => product.category === searchResults.find((p) => p.id === id)?.category
//         );
//       });
//     }
    
//     // If no recommendations based on clicks, fallback to search history
//     if (recommended.length === 0 && searchHistory.length > 0) {
//       recommended = searchResults.filter((product) =>
//         searchHistory.some((history) => product.title.toLowerCase().includes(history.toLowerCase()))
//       );
//     }

//     return recommended;
//   }, [searchResults]); // Add searchResults as dependency to re-calculate recommendations when results change

//   // Function to load clickedProducts and searchHistory from localStorage
//   useEffect(() => {
//     const clickedProducts = JSON.parse(localStorage.getItem("clickedProducts")) || [];
//     const searchHistory = JSON.parse(localStorage.getItem("searchHistory")) || [];

//     // Generate recommendations based on clickedProducts or searchHistory
//     const recommendedProducts = generateRecommendations(clickedProducts, searchHistory);
//     setRecommendations(recommendedProducts);
//   }, [searchResults, generateRecommendations]); // Recalculate recommendations when search results or generateRecommendations change

//   // Function to track product clicks and save them in localStorage
//   const trackProductClick = (productId) => {
//     if (!productId) return; // Don't track invalid IDs

//     // Get the existing clicked products from localStorage
//     let clickedProducts = JSON.parse(localStorage.getItem("clickedProducts")) || [];
    
//     // Only add the product if it's not already in the list (prevent duplicates)
//     if (!clickedProducts.includes(productId)) {
//       clickedProducts.push(productId);
//       localStorage.setItem("clickedProducts", JSON.stringify(clickedProducts)); // Save updated list to localStorage
//     }
//   };

//   return (
//     <div className="flex flex-col items-center min-h-screen bg-gradient-to-b from-white to-sky-300">
//       {!state.present?.searchQuery && (
//         <div className="text-center mb-4 mt-20">
//           <h1 className="text-3xl font-bold text-gray-800">
//             Find The Best Product With Our Recommendations
//           </h1>
//           <p className="mt-4 text-gray-600 text-2xl">Smart shopping made simple</p>
//         </div>
//       )}

//       {/* Search Bar */}
//       <div
//         className={`w-full px-4 transition-all duration-500 mt-20 ${
//           state.present?.searchQuery ? "mt-4" : "mt-20"
//         }`}
//       >
//         <SearchBar onSearch={handleSearch} initialValue={state.present?.searchQuery || ""} />
//       </div>

//       {/* Recommendations */}
//       {recommendations.length > 0 && (
//         <div className="w-full mt-6 px-4">
//           <h2 className="text-2xl font-bold text-center">Recommended for You</h2>
//           <div className="flex justify-center mt-4">
//             {recommendations.map((product) => (
//               <div
//                 key={product.id}
//                 onClick={() => trackProductClick(product.id)}
//                 className="cursor-pointer p-4 border rounded-lg m-2 hover:shadow-lg"
//               >
//                 <img src={product.image_url} alt={product.title} className="w-full h-40 object-contain mb-4" />
//                 <h3 className="text-md font-semibold">{product.title}</h3>
//                 <p className="text-gray-700 font-bold">Rs {product.price}</p>
//               </div>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Product List */}
//       {state.present?.searchQuery && (
//         <div className="w-full mt-6 px-4">
//           {loading ? (
//             <div className="flex justify-center items-center py-8">
//               <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
//               <span className="ml-4 text-gray-600">Searching for products...</span>
//             </div>
//           ) : (
//             <ProductList
//               searchTerm={state.present?.searchQuery}
//               results={searchResults} // Pass results from the search API to ProductList
//               onProductClick={trackProductClick} // Track product click
//             />
//           )}
//         </div>
//       )}
//     </div>
//   );
// };

// export default Home;


// import React, { useState, useEffect, useCallback } from "react";
// import { useUndoRedo } from "../context/UndoRedoContext";
// import ProductList from "./productlist";
// import SearchBar from "./searchbar";

// const Home = () => {
//   const { state, setState } = useUndoRedo();
//   const [loading, setLoading] = useState(false);
//   const [searchResults, setSearchResults] = useState([]);
//   const [recommendations, setRecommendations] = useState([]);

//   // Function to fetch products from API based on search query
//   const fetchProducts = async (query) => {
//     setLoading(true);
//     try {
//       const response = await fetch(`http://localhost:8000/api/search?query=${query}`);
//       const data = await response.json();

//       if (data.success) {
//         setSearchResults(data.data); // Update searchResults with API data
//       } else {
//         throw new Error("Failed to fetch products.");
//       }
//     } catch (error) {
//       console.error("Error fetching products:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Function to handle search
//   const handleSearch = (query) => {
//     setState({
//       searchQuery: query,
//       isSearching: true,
//       searchResults: [],
//     });
//     fetchProducts(query); // Call the fetchProducts function on search
//   };

//   // Memoized function to generate recommendations
//   const generateRecommendations = useCallback((clickedProducts, searchHistory) => {
//     let recommended = [];
    
//     // If clickedProducts have data, fetch recommendations based on categories
//     if (clickedProducts.length > 0) {
//       recommended = searchResults.filter((product) => {
//         return clickedProducts.some(
//           (id) => product.category === searchResults.find((p) => p.id === id)?.category
//         );
//       });
//     }
    
//     // If no recommendations based on clicks, fallback to search history
//     if (recommended.length === 0 && searchHistory.length > 0) {
//       recommended = searchResults.filter((product) =>
//         searchHistory.some((history) => product.title.toLowerCase().includes(history.toLowerCase()))
//       );
//     }

//     return recommended;
//   }, [searchResults]); // Add searchResults as dependency to re-calculate recommendations when results change

//   // Function to load clickedProducts and searchHistory from localStorage
//   useEffect(() => {
//     const clickedProducts = JSON.parse(localStorage.getItem("clickedProducts")) || [];
//     const searchHistory = JSON.parse(localStorage.getItem("searchHistory")) || [];

//     // Generate recommendations based on clickedProducts or searchHistory
//     const recommendedProducts = generateRecommendations(clickedProducts, searchHistory);
//     setRecommendations(recommendedProducts);
//   }, [searchResults, generateRecommendations]); // Recalculate recommendations when search results or generateRecommendations change

//   // Function to track product clicks and save them in localStorage
//   const trackProductClick = (productId) => {
//     if (!productId) return; // Don't track invalid IDs

//     // Get the existing clicked products from localStorage
//     let clickedProducts = JSON.parse(localStorage.getItem("clickedProducts")) || [];
    
//     // Only add the product if it's not already in the list (prevent duplicates)
//     if (!clickedProducts.includes(productId)) {
//       clickedProducts.push(productId);
//       localStorage.setItem("clickedProducts", JSON.stringify(clickedProducts)); // Save updated list to localStorage
//     }
//   };

//   return (
//     <div className="flex flex-col items-center min-h-screen bg-gradient-to-b from-white to-sky-300">
//       {!state.present?.searchQuery && (
//         <div className="text-center mb-4 mt-20">
//           <h1 className="text-3xl font-bold text-gray-800">
//             Find The Best Product With Our Recommendations
//           </h1>
//           <p className="mt-4 text-gray-600 text-2xl">Smart shopping made simple</p>
//         </div>
//       )}

//       {/* Search Bar */}
//       <div
//         className={`w-full px-4 transition-all duration-500 mt-20 ${
//           state.present?.searchQuery ? "mt-4" : "mt-20"
//         }`}
//       >
//         <SearchBar onSearch={handleSearch} initialValue={state.present?.searchQuery || ""} />
//       </div>

//       {/* Recommendations */}
//       {recommendations.length > 0 && (
//         <div className="w-full mt-6 px-4">
//           <h2 className="text-2xl font-bold text-center">Recommended for You</h2>
//           <div className="flex justify-center mt-4">
//             {recommendations.map((product) => (
//               <div
//                 key={product.id}
//                 onClick={() => trackProductClick(product.id)}
//                 className="cursor-pointer p-4 border rounded-lg m-2 hover:shadow-lg"
//               >
//                 <img src={product.image_url} alt={product.title} className="w-full h-40 object-contain mb-4" />
//                 <h3 className="text-md font-semibold">{product.title}</h3>
//                 <p className="text-gray-700 font-bold">Rs {product.price}</p>
//               </div>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Product List */}
//       {state.present?.searchQuery && (
//         <div className="w-full mt-6 px-4">
//           {loading ? (
//             <div className="flex justify-center items-center py-8">
//               <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
//               <span className="ml-4 text-gray-600">Searching for products...</span>
//             </div>
//           ) : (
//             <ProductList
//               searchTerm={state.present?.searchQuery}
//               results={searchResults} // Pass results from the search API to ProductList
//               onProductClick={trackProductClick} // Track product click
//             />
//           )}
//         </div>
//       )}
//     </div>
//   );
// };

// export default Home;



// import React, { useState, useEffect } from "react";
// import { useUndoRedo } from "../context/UndoRedoContext";
// import ProductList from "./productlist";
// import SearchBar from "./searchbar";

// const Home = () => {
//   const { state, setState } = useUndoRedo();
//   const [loading, setLoading] = useState(false);
//   const [searchResults, setSearchResults] = useState([]);
//   const [recommendations, setRecommendations] = useState([]);
//   const [initialLoad, setInitialLoad] = useState(true);

//   // Function to fetch products from API based on search query
//   const fetchProducts = async (query) => {
//     setLoading(true);
//     try {
//       const response = await fetch(`http://localhost:8000/api/search?query=${query}`);
//       const data = await response.json();

//       if (data.success) {
//         setSearchResults(data.data);
//       } else {
//         throw new Error("Failed to fetch products.");
//       }
//     } catch (error) {
//       console.error("Error fetching products:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Function to fetch popular products for initial recommendations
//   // const fetchPopularProducts = async () => {
//   //   setLoading(true);
//   //   try {
//   //     const response = await fetch("http://localhost:8000/api/popular");
//   //     const data = await response.json();

//   //     if (data.success) {
//   //       setSearchResults(data.data);
//   //       generateRecommendations(data.data);
//   //     } else {
//   //       throw new Error("Failed to fetch popular products.");
//   //     }
//   //   } catch (error) {
//   //     console.error("Error fetching popular products:", error);
//   //   } finally {
//   //     setLoading(false);
//   //   }
//   // };

//   // Function to handle search
//   const handleSearch = (query) => {
//     setState({
//       searchQuery: query,
//       isSearching: true,
//       searchResults: [],
//     });

//     // Save search history to localStorage
//     trackSearchHistory(query);

//     fetchProducts(query);
//   };

//   // Function to track search history and save it in localStorage
//   const trackSearchHistory = (query) => {
//     try {
//       const searchHistory = JSON.parse(localStorage.getItem("searchHistory")) || [];
      
//       // Prevent duplicates and limit to 10 entries
//       const updatedHistory = [
//         ...searchHistory.filter(item => item !== query),
//         query
//       ].slice(-10);
      
//       localStorage.setItem("searchHistory", JSON.stringify(updatedHistory));
//     } catch (error) {
//       console.error("Error saving search history:", error);
//     }
//   };

//   // Function to track product clicks and save them in localStorage
//   const trackProductClick = (product) => {
//     try {
//       if (!product || !product.id) {
//         console.error("Invalid product:", product);
//         return;
//       }
      
//       // Convert to string to avoid type issues
//       const productId = String(product.id);
      
//       let clickedProducts = JSON.parse(localStorage.getItem("clickedProducts")) || [];
//       console.log("Current clickedProducts:", clickedProducts);
      
//       // Only add if not already in the list
//       if (!clickedProducts.includes(productId)) {
//         // Limit to 20 most recent clicks
//         clickedProducts = [...clickedProducts, productId].slice(-20);
//         localStorage.setItem("clickedProducts", JSON.stringify(clickedProducts));
//         console.log("Updated clickedProducts:", clickedProducts);
//       } else {
//         console.log("Product already tracked:", productId);
//       }
      
//       // Immediately update recommendations
//       generateRecommendations(searchResults);
//     } catch (error) {
//       console.error("Error tracking product click:", error);
//     }
//   };

//   // Function to generate recommendations based on clicked products or search history
//   const generateRecommendations = (products) => {
//     try {
//       const clickedProducts = JSON.parse(localStorage.getItem("clickedProducts")) || [];
//       const searchHistory = JSON.parse(localStorage.getItem("searchHistory")) || [];
//       let recommended = [];

//       console.log("Generating recommendations...");
//       console.log("Clicked Products:", clickedProducts);
//       console.log("Search History:", searchHistory);

//       // 1. Priority: Products from same category as clicked items
//       if (clickedProducts.length > 0) {
//         // Get categories of clicked products
//         const clickedCategories = [];
//         for (const productId of clickedProducts) {
//           const product = products.find(p => String(p.id) === productId);
//           if (product && product.category) {
//             clickedCategories.push(product.category);
//           }
//         }
        
//         // Filter products that match any clicked category
//         recommended = [
//           ...recommended,
//           ...products.filter(product => 
//             clickedCategories.includes(product.category) && 
//             !clickedProducts.includes(String(product.id))
//           )
//         ];
//       }

//       // 2. Fallback: Products matching search history
//       if (recommended.length < 5 && searchHistory.length > 0) {
//         const historyKeywords = [...new Set(searchHistory.flatMap(term => 
//           term.toLowerCase().split(/\s+/)
//         ))];
        
//         recommended = [
//           ...recommended,
//           ...products.filter(product => 
//             historyKeywords.some(keyword => 
//               product.title.toLowerCase().includes(keyword)
//           ).filter(product => 
//             !recommended.some(r => r.id === product.id) &&
//             !clickedProducts.includes(String(product.id))
//           )
//         )];
//       }

//       // 3. Final fallback: Top-rated products
//       if (recommended.length < 5) {
//         recommended = [
//           ...recommended,
//           ...products
//             .sort((a, b) => b.stars - a.stars || b.review_count - a.review_count)
//             .filter(product => 
//               !recommended.some(r => r.id === product.id) &&
//               !clickedProducts.includes(String(product.id))
//             )
//             .slice(0, 10 - recommended.length)
//         ];
//       }

//       // Remove duplicates and limit to 10
//       const uniqueRecs = recommended.reduce((acc, product) => {
//         if (!acc.some(p => p.id === product.id)) {
//           acc.push(product);
//         }
//         return acc;
//       }, []).slice(0, 10);

//       console.log("Final recommendations:", uniqueRecs);
//       setRecommendations(uniqueRecs);
//     } catch (error) {
//       console.error("Error generating recommendations:", error);
//       setRecommendations([]);
//     }
//   };

//   // Load initial recommendations on page load
//   useEffect(() => {
//     if (initialLoad && !state.present?.searchQuery) {
//       // fetchPopularProducts();
//       setInitialLoad(false);
//     }
//   }, [initialLoad, state.present?.searchQuery]);

//   // Update recommendations when search results change
//   useEffect(() => {
//     if (searchResults.length > 0 && !state.present?.searchQuery) {
//       generateRecommendations(searchResults);
//     }
//   }, [searchResults, state.present?.searchQuery]);

//   return (
//     <div className="flex flex-col items-center min-h-screen bg-gradient-to-b from-white to-sky-300">
//       {!state.present?.searchQuery && (
//         <div className="text-center mb-4 mt-20">
//           <h1 className="text-3xl font-bold text-gray-800">
//             Find The Best Product With Our Recommendations
//           </h1>
//           <p className="mt-4 text-gray-600 text-2xl">Smart shopping made simple</p>
//         </div>
//       )}

//       {/* Search Bar */}
//       <div
//         className={`w-full px-4 transition-all duration-500 ${
//           state.present?.searchQuery ? "mt-4" : "mt-20"
//         }`}
//       >
//         <SearchBar onSearch={handleSearch} initialValue={state.present?.searchQuery || ""} />
//       </div>

//       {/* Recommendations */}
//       {!loading && recommendations.length > 0 && !state.present?.searchQuery && (
//         <div className="w-full mt-6 px-4">
//           <h2 className="text-2xl font-bold text-center">Recommended for You</h2>
//           <div className="flex flex-wrap justify-center mt-4">
//             {recommendations.map((product) => (
//               <a
//                 key={product.id}
//                 href={product.link}
//                 target="_blank"
//                 rel="noopener noreferrer"
//                 className="cursor-pointer p-4 border rounded-lg m-2 hover:shadow-lg w-52 bg-white"
//                 onClick={(e) => {
//                   e.preventDefault();
//                   trackProductClick(product);
//                   window.open(product.link, '_blank');
//                 }}
//               >
//                 <img 
//                   src={product.image_url} 
//                   alt={product.title} 
//                   className="w-full h-40 object-contain mb-4" 
//                 />
//                 <h3 className="text-md font-semibold truncate">{product.title}</h3>
//                 <p className="text-gray-700 font-bold">Rs {product.price}</p>
//               </a>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Product List */}
//       {state.present?.searchQuery && (
//         <div className="w-full mt-6 px-4">
//           {loading ? (
//             <div className="flex justify-center items-center py-8">
//               <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
//               <span className="ml-4 text-gray-600">Searching for products...</span>
//             </div>
//           ) : (
//             <ProductList
//               searchTerm={state.present?.searchQuery}
//               results={searchResults}
//               onProductClick={trackProductClick}
//             />
//           )}
//         </div>
//       )}
//     </div>
//   );
// };

// export default Home;

// ======================================================================================================working till local storage
// import React from "react";
// import { useUndoRedo } from "../context/UndoRedoContext";
// import ProductList from "./productlist";
// import SearchBar from "./searchbar";

// const Home = () => {
//   const { state, setState } = useUndoRedo();

//   const handleSearch = (query) => {
//     const newState = {
//       searchQuery: query,
//       isSearching: true,
//       searchResults: []
//     };
//     setState(newState);
    
//     // Simulate API call
//     setTimeout(() => {
//       const updatedState = {
//         ...newState,
//         isSearching: false,
//         searchResults: []
//       };
//       setState(updatedState);

//       // Store the search query in localStorage (you could also store some other metadata)
//       const recentSearches = JSON.parse(localStorage.getItem("recentSearches")) || [];
//       if (!recentSearches.includes(query)) {
//         recentSearches.push(query);
//         if (recentSearches.length > 5) recentSearches.shift(); // Limit to last 5 searches
//         localStorage.setItem("recentSearches", JSON.stringify(recentSearches));
//       }
//     }, 1000);
//   };

//   return (
//     <div className="flex flex-col items-center min-h-screen bg-gradient-to-b from-white to-sky-300">
//       {!state.present?.searchQuery && (
//         <div className="text-center mb-4 mt-20">
//           <h1 className="text-3xl font-bold text-gray-800">
//             Find The Best Product With Our Recommendations
//           </h1>
//           <p className="mt-4 text-gray-600 text-2xl">Smart shopping made simple</p>
//         </div>
//       )}

//       {/* Search Bar */}
//       <div
//         className={`w-full px-4 transition-all duration-500 mt-20 ${
//           state.present?.searchQuery ? "mt-4" : "mt-20"
//         }`}
//       >
//         <SearchBar 
//           onSearch={handleSearch} 
//           initialValue={state.present?.searchQuery || ""} 
//         />
//       </div>

//       {/* Product List */}
//       {state.present?.searchQuery && (
//         <div className="w-full mt-6 px-4">
//           {state.present?.isSearching ? (
//             <div className="flex justify-center items-center py-8">
//               <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
//               <span className="ml-4 text-gray-600">Searching for products...</span>
//             </div>
//           ) : (
//             <ProductList 
//               searchTerm={state.present?.searchQuery} 
//               results={state.present?.searchResults} 
//             />
//           )}
//         </div>
//       )}
//     </div>
//   );
// };

// export default Home;
// ================================================================

// import React, { useState, useEffect } from "react";
// import ProductList from "./productlist";
// import SearchBar from "./searchbar";

// const Home = () => {
//   const [searchTerm, setSearchTerm] = useState("");
//   const [viewedProducts, setViewedProducts] = useState([]);
//   const [searchHistory, setSearchHistory] = useState([]);
//   const [recommendedProducts, setRecommendedProducts] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     // Load search history and viewed products from localStorage
//     const savedSearchHistory = JSON.parse(localStorage.getItem("recentSearches")) || [];
//     const savedViewedProducts = JSON.parse(localStorage.getItem("viewedProducts")) || [];
//     setSearchHistory(savedSearchHistory);
//     setViewedProducts(savedViewedProducts);

//     // Automatically fetch recommendations if there's data in localStorage
//     if (savedSearchHistory.length > 0 || savedViewedProducts.length > 0) {
//       fetchRecommendedProducts(savedSearchHistory, savedViewedProducts);
//     }
//   }, []);

//   const fetchRecommendedProducts = async (searchHistory, viewedProducts) => {
//     setIsLoading(true);

//     // Extract categories from search history and product IDs from viewed products
//     const categories = searchHistory; // Search history is a list of categories
//     const productIds = viewedProducts.map(product => product._id); // Extract product IDs from viewed products

//     try {
//       const response = await fetch(
//         `http://localhost:5000/api/recommendation?categories=${categories.join(",")}&productIds=${productIds.join(",")}`
//       );

//       if (!response.ok) {
//         throw new Error("Failed to fetch recommended products.");
//       }

//       const result = await response.json();

//       if (result.success) {
//         setRecommendedProducts(result.data); // Assuming data is in result.data
//       } else {
//         setRecommendedProducts([]); // If no recommended products
//       }
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleSearch = (query) => {
//     setSearchTerm(query);

//     // Save to localStorage (search history)
//     const newSearchHistory = [query, ...searchHistory];
//     if (newSearchHistory.length > 5) {
//       newSearchHistory.pop(); // Limit to last 5 searches
//     }
//     localStorage.setItem("recentSearches", JSON.stringify(newSearchHistory));

//     // Fetch products based on the search term
//     fetchRecommendedProducts(newSearchHistory, viewedProducts);
//   };

//   return (
//     <div className="flex flex-col items-center min-h-screen bg-gradient-to-b from-white to-sky-300">
//       <div className="text-center mb-4 mt-20">
//         <h1 className="text-3xl font-bold text-gray-800">
//           Find The Best Product With Our Recommendations
//         </h1>
//         <p className="mt-4 text-gray-600 text-2xl">Smart shopping made simple</p>
//       </div>

//       {/* Search Bar */}
//       <div className="w-full px-4 mt-4">
//         <SearchBar onSearch={handleSearch} initialValue={searchTerm} />
//       </div>

//       {/* Recommended Products or Search Results */}
//       {isLoading ? (
//         <div className="text-center text-lg">Loading recommended products...</div>
//       ) : error ? (
//         <div className="text-center text-red-500">{error}</div>
//       ) : (
//         // <ProductList searchTerm={searchTerm} results={recommendedProducts} />
//         // Change this in Home component's return:
// <ProductList 
//   searchTerm={searchTerm} 
//   results={searchTerm ? [] : recommendedProducts} // Fix prop logic
//   searchResults={searchTerm ? recommendedProducts : []} // New prop
// />
//       )}
//     </div>
//   );
// };

// export default Home;

import React, { useState, useEffect } from "react";
import ProductList from "./productlist";
import SearchBar from "./searchbar";

const Home = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [viewedProducts, setViewedProducts] = useState([]);
  const [searchHistory, setSearchHistory] = useState([]);
  const [recommendedProducts, setRecommendedProducts] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize from localStorage
  useEffect(() => {
    const savedSearchHistory = JSON.parse(localStorage.getItem("recentSearches")) || [];
    const savedViewedProducts = JSON.parse(localStorage.getItem("viewedProducts")) || [];
    
    setSearchHistory(savedSearchHistory);
    setViewedProducts(savedViewedProducts);

    if (savedSearchHistory.length > 0 || savedViewedProducts.length > 0) {
      fetchRecommendedProducts(savedSearchHistory, savedViewedProducts);
    }
  }, []);

  // Fetch recommendations with proper error handling
  const fetchRecommendedProducts = async (history, viewed) => {
    setIsLoading(true);
    setError(null);
    
    // Safely prepare parameters
    const categories = Array.isArray(history) ? history : [];
    const productIds = (Array.isArray(viewed) ? viewed : [])
      .map(p => p?._id)
      .filter(id => id && typeof id === "string");

    try {
      const params = new URLSearchParams();
      if (categories.length) params.append("categories", categories.join(","));
      if (productIds.length) params.append("productIds", productIds.join(","));
      
      const url = `http://localhost:8000/api/recommendation?${params.toString()}`;
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.success) {
        setRecommendedProducts(result.data || []);
      } else {
        throw new Error(result.message || "No recommendations found");
      }
    } catch (err) {
      setError(`Recommendations failed: ${err.message}`);
      console.error("Recommendation error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  // Search function
  const fetchSearchResults = async (query) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8000/api/search?query=${encodeURIComponent(query)}`);
      
      if (!response.ok) {
        throw new Error(`Search failed: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.success) {
        setSearchResults(result.data || []);
      } else {
        throw new Error(result.message || "No products found");
      }
    } catch (err) {
      setError(`Search error: ${err.message}`);
      console.error("Search error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle search action
  const handleSearch = (query) => {
    const trimmedQuery = query.trim();
    if (!trimmedQuery) return;
    
    setSearchTerm(trimmedQuery);
    fetchSearchResults(trimmedQuery);

    // Update search history
    const newHistory = [
      trimmedQuery, 
      ...searchHistory.filter(term => term !== trimmedQuery)
    ].slice(0, 5);
    
    localStorage.setItem("recentSearches", JSON.stringify(newHistory));
    setSearchHistory(newHistory);
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-gradient-to-b  from-sky-300 to white" >
      {!searchTerm && (
        <div className="text-center mb-4 mt-20">
          <h1 className="text-3xl font-bold text-gray-800">
            Find The Best Product With Our Recommendations
          </h1>
          <p className="mt-4 text-gray-600 text-2xl">Smart shopping made simple</p>
        </div>
      )}

      {/* Search Bar */}
      <div
        className={`w-full px-4 transition-all duration-500 ${
          searchTerm ? "mt-4" : "mt-20"
        }`}
      >
        <SearchBar 
          onSearch={handleSearch} 
          initialValue={searchTerm} 
        />
      </div>

      {/* Content Area */}
      {isLoading ? (
        <div className="w-full mt-6 px-4">
          <div className="flex justify-center items-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            <span className="ml-4 text-gray-600">
              {searchTerm ? "Searching for products..." : "Loading recommendations..."}
            </span>
          </div>
        </div>
      ) : error ? (
        <div className="text-center text-red-500 py-4 w-full">{error}</div>
      ) : searchTerm ? (
        <div className="w-full mt-6 px-4">
          <ProductList results={searchResults} />
        </div>
      ) : (
        <div className="w-full mt-6 px-4">
  <div className="text-center text-2xl font-bold text-gray-800 py-4 w-full">
    <h2>Recommended Products for you!</h2>
  </div>
  <ProductList results={recommendedProducts} />
</div>

      )}
    </div>
  );
};

export default Home;