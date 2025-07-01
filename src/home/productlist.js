// import React, { useEffect, useState } from "react";

// const ProductList = ({ searchTerm }) => {
//   const [products, setProducts] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);
//   const [sortOption, setSortOption] = useState("none");
//   const [filterOption, setFilterOption] = useState("all");

//   useEffect(() => {
//     const fetchProducts = async () => {
//       if (!searchTerm) return;

//       setLoading(true);
//       setError(null);

//       try {
//         const response = await fetch(
//           `http://localhost:8000/api/search?query=${searchTerm}`
//         );
        

//         if (!response.ok) {
//           throw new Error("Failed to fetch products.");
//         }

//         const result = await response.json();

//         if (result.success) {
//           setProducts(result.data);
//         } else {
//           throw new Error(result.message || "Failed to fetch products.");
//         }
//       } catch (err) {
//         setError(err.message);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchProducts();

//     return () => setLoading(false);
//   }, [searchTerm]);

//   const handleSort = (option) => {
//     setSortOption(option);
//   };

//   const handleFilter = (option) => {
//     setFilterOption(option);
//   };

//   const sortedProducts = (() => {
//     let filteredProducts = [...products];

//     // Apply filtering based on ratings
//     if (filterOption === "high") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 4
//       );
//     } else if (filterOption === "normal") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 3 && product.stars < 4
//       );
//     } else if (filterOption === "low") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 1 && product.stars < 3
//       );
//     }

//     // Apply sorting
//     if (sortOption === "price-asc") {
//       return filteredProducts.sort((a, b) => a.price - b.price);
//     } else if (sortOption === "price-desc") {
//       return filteredProducts.sort((a, b) => b.price - a.price);
//     }

//     return filteredProducts;
//   })();

//   if (loading) {
//     return (
//       <div className="flex justify-center items-center min-h-screen">
//         <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
//       </div>
//     );
//   }

//   if (error) {
//     return <div className="text-center text-red-500">Error: {error}</div>;
//   }

//   if (!products.length) {
//     return <div className="text-center text-lg">No products found.</div>;
//   }

//   return (
//     <div className="flex justify-center">
//       <div className="w-11/12">
//         {/* Sorting and Filtering Controls */}
//         <div className="mb-4 flex justify-between">
//           {/* Sort Dropdown */}
//           <select
//             value={sortOption}
//             onChange={(e) => handleSort(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="none">No Sorting</option>
//             <option value="price-asc">Price: Low to High</option>
//             <option value="price-desc">Price: High to Low</option>
//           </select>

//           {/* Filter Dropdown */}
//           <select
//             value={filterOption}
//             onChange={(e) => handleFilter(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="all">All Ratings</option>
//             <option value="high">High Ratings (4-5)</option>
//             <option value="normal">Normal Ratings (3-4)</option>
//             <option value="low">Low Ratings (1-3)</option>
//           </select>
//         </div>

//         {/* Product Grid */}
//         <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
//           {sortedProducts.map((product, index) => (
//             <a
//               target="_blank"
//               rel="noopener noreferrer"
//               href={product.link}
//               key={index}
//               className="border rounded-lg p-4 flex flex-col items-center bg-white shadow-lg hover:shadow-xl transition"
//             >
//               {/* Product Image */}
//               <img
//                 src={product.image_url}
//                 alt={product.title}
//                 className="w-full h-40 object-contain mb-4"
//               />

//               {/* Product Title */}
//               <h2 className="text-md mb-2 text-left w-full whitespace-nowrap overflow-hidden text-ellipsis">
//                 {product.title}
//               </h2>

//               {/* Product Price */}
//               <p className="text-gray-700 font-bold mb-2">Rs {product.price}</p>

//               {/* Rating & Stars */}
//               <div className="flex items-center justify-between w-full text-sm">
//                 <div className="flex items-center">
//                   <span className="mr-1">★</span>
//                   <span className="font-semibold">
//                     {product.stars || "N/A"}
//                   </span>
//                   <span>/5</span>
//                   <span className="text-gray-600 ml-2">
//                     ({product.review_count || "0"} )
//                   </span>
//                 </div>
//                 <div className="bg-blue-500 text-white px-1 py-1 rounded-full text-xs font-semibold">
//                   {product.sentiment_score * 2 || "0"}/10
//                 </div>
//               </div>
//             </a>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ProductList;


// import React, { useState } from "react";

// const ProductList = ({ searchTerm, results, onProductClick }) => {
//   const [sortOption, setSortOption] = useState("none");
//   const [filterOption, setFilterOption] = useState("all");

//   const handleSort = (option) => {
//     setSortOption(option);
//   };

//   const handleFilter = (option) => {
//     setFilterOption(option);
//   };

//   const sortedProducts = (() => {
//     let filteredProducts = [...results];

//     // Apply filtering based on ratings
//     if (filterOption === "high") {
//       filteredProducts = filteredProducts.filter((product) => product.stars >= 4);
//     } else if (filterOption === "normal") {
//       filteredProducts = filteredProducts.filter((product) => product.stars >= 3 && product.stars < 4);
//     } else if (filterOption === "low") {
//       filteredProducts = filteredProducts.filter((product) => product.stars >= 1 && product.stars < 3);
//     }

//     // Apply sorting
//     if (sortOption === "price-asc") {
//       return filteredProducts.sort((a, b) => a.price - b.price);
//     } else if (sortOption === "price-desc") {
//       return filteredProducts.sort((a, b) => b.price - a.price);
//     }

//     return filteredProducts;
//   })();

//   if (!results.length) {
//     return <div className="text-center text-lg">No products found.</div>;
//   }

//   return (
//     <div className="flex justify-center">
//       <div className="w-11/12">
//         {/* Sorting and Filtering Controls */}
//         <div className="mb-4 flex justify-between">
//           {/* Sort Dropdown */}
//           <select
//             value={sortOption}
//             onChange={(e) => handleSort(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="none">No Sorting</option>
//             <option value="price-asc">Price: Low to High</option>
//             <option value="price-desc">Price: High to Low</option>
//           </select>

//           {/* Filter Dropdown */}
//           <select
//             value={filterOption}
//             onChange={(e) => handleFilter(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="all">All Ratings</option>
//             <option value="high">High Ratings (4-5)</option>
//             <option value="normal">Normal Ratings (3-4)</option>
//             <option value="low">Low Ratings (1-3)</option>
//           </select>
//         </div>

//         {/* Product Grid */}
//         <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
//           {sortedProducts.map((product, index) => (
//             <a
//               key={index}
//               href={product.link} // The product link to Daraz
//               target="_blank"
//               rel="noopener noreferrer"
//               className="border rounded-lg p-4 flex flex-col items-center bg-white shadow-lg hover:shadow-xl transition"
//               onClick={() => onProductClick(product.id)} // Track product click
//             >
//               {/* Product Image */}
//               <img
//                 src={product.image_url}
//                 alt={product.title}
//                 className="w-full h-40 object-contain mb-4"
//               />

//               {/* Product Title */}
//               <h2 className="text-md mb-2 text-left w-full whitespace-nowrap overflow-hidden text-ellipsis">
//                 {product.title}
//               </h2>

//               {/* Product Price */}
//               <p className="text-gray-700 font-bold mb-2">Rs {product.price}</p>

//               {/* Rating & Stars */}
//               <div className="flex items-center justify-between w-full text-sm">
//                 <div className="flex items-center">
//                   <span className="mr-1">★</span>
//                   <span className="font-semibold">{product.stars || "N/A"}</span>
//                   <span>/5</span>
//                   <span className="text-gray-600 ml-2">({product.review_count || "0"} )</span>
//                 </div>
//                 <div className="bg-blue-500 text-white px-1 py-1 rounded-full text-xs font-semibold">
//                   {product.sentiment_score * 2 || "0"}/10
//                 </div>
//               </div>
//             </a>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ProductList;


// import React, { useState } from "react";

// const ProductList = ({ searchTerm, results, onProductClick }) => {
//   const [sortOption, setSortOption] = useState("none");
//   const [filterOption, setFilterOption] = useState("all");

//   const handleSort = (option) => {
//     setSortOption(option);
//   };

//   const handleFilter = (option) => {
//     setFilterOption(option);
//   };

//   const sortedProducts = (() => {
//     let filteredProducts = [...results];

//     // Apply filtering based on ratings
//     if (filterOption === "high") {
//       filteredProducts = filteredProducts.filter((product) => product.stars >= 4);
//     } else if (filterOption === "normal") {
//       filteredProducts = filteredProducts.filter((product) => product.stars >= 3 && product.stars < 4);
//     } else if (filterOption === "low") {
//       filteredProducts = filteredProducts.filter((product) => product.stars >= 1 && product.stars < 3);
//     }

//     // Apply sorting
//     if (sortOption === "price-asc") {
//       return filteredProducts.sort((a, b) => a.price - b.price);
//     } else if (sortOption === "price-desc") {
//       return filteredProducts.sort((a, b) => b.price - a.price);
//     }

//     return filteredProducts;
//   })();

//   if (!results.length) {
//     return <div className="text-center text-lg py-8">No products found for "{searchTerm}"</div>;
//   }

//   return (
//     <div className="flex justify-center">
//       <div className="w-11/12">
//         {/* Sorting and Filtering Controls */}
//         <div className="mb-4 flex justify-between">
//           {/* Sort Dropdown */}
//           <select
//             value={sortOption}
//             onChange={(e) => handleSort(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="none">No Sorting</option>
//             <option value="price-asc">Price: Low to High</option>
//             <option value="price-desc">Price: High to Low</option>
//           </select>

//           {/* Filter Dropdown */}
//           <select
//             value={filterOption}
//             onChange={(e) => handleFilter(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="all">All Ratings</option>
//             <option value="high">High Ratings (4-5)</option>
//             <option value="normal">Normal Ratings (3-4)</option>
//             <option value="low">Low Ratings (1-3)</option>
//           </select>
//         </div>

//         {/* Product Grid */}
//         <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
//           {sortedProducts.map((product) => (
//             <a
//               key={product.id}
//               href={product.link}
//               target="_blank"
//               rel="noopener noreferrer"
//               className="border rounded-lg p-4 flex flex-col items-center bg-white shadow-lg hover:shadow-xl transition"
//               onClick={(e) => {
//                 e.preventDefault();
//                 onProductClick(product);
//                 window.open(product.link, '_blank');
//               }}
//             >
//               {/* Product Image */}
//               <img
//                 src={product.image_url}
//                 alt={product.title}
//                 className="w-full h-40 object-contain mb-4"
//               />

//               {/* Product Title */}
//               <h2 className="text-md mb-2 text-left w-full whitespace-nowrap overflow-hidden text-ellipsis">
//                 {product.title}
//               </h2>

//               {/* Product Price */}
//               <p className="text-gray-700 font-bold mb-2">Rs {product.price}</p>

//               {/* Rating & Stars */}
//               <div className="flex items-center justify-between w-full text-sm">
//                 <div className="flex items-center">
//                   <span className="mr-1">★</span>
//                   <span className="font-semibold">{product.stars || "N/A"}</span>
//                   <span>/5</span>
//                   <span className="text-gray-600 ml-2">({product.review_count || "0"})</span>
//                 </div>
//                 <div className="bg-blue-500 text-white px-1 py-1 rounded-full text-xs font-semibold">
//                   {product.sentiment_score * 2 || "0"}/10
//                 </div>
//               </div>
//             </a>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ProductList;



// import React, { useEffect, useState } from "react";

// const ProductList = ({ searchTerm }) => {
//   const [products, setProducts] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);
//   const [sortOption, setSortOption] = useState("none");
//   const [filterOption, setFilterOption] = useState("all");

//   useEffect(() => {
//     const fetchProducts = async () => {
//       if (!searchTerm) return;

//       setLoading(true);
//       setError(null);

//       try {
//         // API call to fetch products based on the search term
//         const response = await fetch(
//           `http://localhost:8000/api/search?query=${searchTerm}`
//         );

//         if (!response.ok) {
//           throw new Error("Failed to fetch products.");
//         }

//         const result = await response.json();

//         if (result.success) {
//           setProducts(result.data);
//         } else {
//           throw new Error(result.message || "Failed to fetch products.");
//         }
//       } catch (err) {
//         setError(err.message);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchProducts();

//     return () => setLoading(false);
//   }, [searchTerm]);

//   const handleSort = (option) => {
//     setSortOption(option);
//   };

//   const handleFilter = (option) => {
//     setFilterOption(option);
//   };

//   const sortedProducts = (() => {
//     let filteredProducts = [...products];

//     // Apply filtering based on ratings
//     if (filterOption === "high") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 4
//       );
//     } else if (filterOption === "normal") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 3 && product.stars < 4
//       );
//     } else if (filterOption === "low") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 1 && product.stars < 3
//       );
//     }

//     // Apply sorting
//     if (sortOption === "price-asc") {
//       return filteredProducts.sort((a, b) => a.price - b.price);
//     } else if (sortOption === "price-desc") {
//       return filteredProducts.sort((a, b) => b.price - a.price);
//     }

//     return filteredProducts;
//   })();

//   // const handleProductClick = (product) => {
//   //   // Store product details in localStorage for future recommendations
//   //   const viewedProducts = JSON.parse(localStorage.getItem("viewedProducts")) || [];

//   //   // Add the clicked product to the list
//   //   if (!viewedProducts.some(p => p.id === product.id)) {
//   //     viewedProducts.push(product);

//   //     // Limit to last 5 viewed products
//   //     if (viewedProducts.length > 5) viewedProducts.shift();

//   //     // Save it back to localStorage
//   //     localStorage.setItem("viewedProducts", JSON.stringify(viewedProducts));
//   //   }
//   // };
//   const handleProductClick = (product) => {
//   // Step 1: Retrieve the previously viewed products from localStorage or initialize an empty array
//   let viewedProducts = JSON.parse(localStorage.getItem("viewedProducts")) || [];

//   // Step 2: Check if the product is already in the list
//   const isProductAlreadyViewed = viewedProducts.some(p => p.id === product.id);

//   if (!isProductAlreadyViewed) {
//     // Step 3: Add the clicked product to the viewed products list
//     viewedProducts.push(product);

//     // Step 4: Limit the number of products to the latest 5 products
//     if (viewedProducts.length > 5) {
//       viewedProducts.shift();  // Remove the oldest product (first in the array)
//     }

//     // Step 5: Update localStorage with the updated list of viewed products
//     localStorage.setItem("viewedProducts", JSON.stringify(viewedProducts));
//   }
// };


//   if (loading) {
//     return (
//       <div className="flex justify-center items-center min-h-screen">
//         <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
//       </div>
//     );
//   }

//   if (error) {
//     return <div className="text-center text-red-500">Error: {error}</div>;
//   }

//   if (!products.length) {
//     return <div className="text-center text-lg">No products found.</div>;
//   }

//   return (
//     <div className="flex justify-center">
//       <div className="w-11/12">
//         {/* Sorting and Filtering Controls */}
//         <div className="mb-4 flex justify-between">
//           {/* Sort Dropdown */}
//           <select
//             value={sortOption}
//             onChange={(e) => handleSort(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="none">No Sorting</option>
//             <option value="price-asc">Price: Low to High</option>
//             <option value="price-desc">Price: High to Low</option>
//           </select>

//           {/* Filter Dropdown */}
//           <select
//             value={filterOption}
//             onChange={(e) => handleFilter(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="all">All Ratings</option>
//             <option value="high">High Ratings (4-5)</option>
//             <option value="normal">Normal Ratings (3-4)</option>
//             <option value="low">Low Ratings (1-3)</option>
//           </select>
//         </div>

//         {/* Product Grid */}
//         <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
//           {sortedProducts.map((product) => (
//             <a
//               key={product.id}
//               onClick={() => handleProductClick(product)} // Track the product click
//               target="_blank"
//               rel="noopener noreferrer"
//               href={product.link}
//               className="border rounded-lg p-4 flex flex-col items-center bg-white shadow-lg hover:shadow-xl transition"
//             >
//               {/* Product Image */}
//               <img
//                 src={product.image_url}
//                 alt={product.title}
//                 className="w-full h-40 object-contain mb-4"
//               />

//               {/* Product Title */}
//               <h2 className="text-md mb-2 text-left w-full whitespace-nowrap overflow-hidden text-ellipsis">
//                 {product.title}
//               </h2>

//               {/* Product Price */}
//               <p className="text-gray-700 font-bold mb-2">Rs {product.price}</p>

//               {/* Rating & Stars */}
//               <div className="flex items-center justify-between w-full text-sm">
//                 <div className="flex items-center">
//                   <span className="mr-1">★</span>
//                   <span className="font-semibold">
//                     {product.stars || "N/A"}
//                   </span>
//                   <span>/5</span>
//                   <span className="text-gray-600 ml-2">
//                     ({product.review_count || "0"} )
//                   </span>
//                 </div>
//                 <div className="bg-blue-500 text-white px-1 py-1 rounded-full text-xs font-semibold">
//                   {product.sentiment_score * 2 || "0"}/10
//                 </div>
//               </div>
//             </a>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ProductList;



// import React, { useEffect, useState } from "react";

// const ProductList = ({ searchTerm }) => {
//   const [products, setProducts] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);
//   const [sortOption, setSortOption] = useState("none");
//   const [filterOption, setFilterOption] = useState("all");

//   useEffect(() => {
//     const fetchProducts = async () => {
//       if (!searchTerm) return;

//       setLoading(true);
//       setError(null);

//       try {
//         const response = await fetch(
//           `http://localhost:8000/api/search?query=${searchTerm}`
//         );

//         if (!response.ok) {
//           throw new Error("Failed to fetch products.");
//         }

//         const result = await response.json();

//         if (result.success) {
//           setProducts(result.data);
//         } else {
//           throw new Error(result.message || "Failed to fetch products.");
//         }
//       } catch (err) {
//         setError(err.message);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchProducts();

//     return () => setLoading(false);
//   }, [searchTerm]);

//   const handleSort = (option) => {
//     setSortOption(option);
//   };

//   const handleFilter = (option) => {
//     setFilterOption(option);
//   };

//   const sortedProducts = (() => {
//     let filteredProducts = [...products];

//     if (filterOption === "high") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 4
//       );
//     } else if (filterOption === "normal") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 3 && product.stars < 4
//       );
//     } else if (filterOption === "low") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 1 && product.stars < 3
//       );
//     }

//     if (sortOption === "price-asc") {
//       return filteredProducts.sort((a, b) => a.price - b.price);
//     } else if (sortOption === "price-desc") {
//       return filteredProducts.sort((a, b) => b.price - a.price);
//     }

//     return filteredProducts;
//   })();

//   // const handleProductClick = (product) => {
//   //   // Step 1: Retrieve the previously viewed products from localStorage, or initialize an empty array if not found
//   //   let viewedProducts = JSON.parse(localStorage.getItem("viewedProducts")) || [];

//   //   // Step 2: Check if the clicked product already exists in the array
//   //   const isProductAlreadyViewed = viewedProducts.some(p => p.id === product.id);

//   //   // Step 3: If the product hasn't been viewed already, add it to the array
//   //   if (!isProductAlreadyViewed) {
//   //     // Add the new product to the list
//   //     viewedProducts.push(product);

//   //     // Step 4: Limit the array to the last 5 viewed products
//   //     if (viewedProducts.length > 5) {
//   //       viewedProducts.shift();  // Remove the oldest product (first in the array)
//   //     }

//   //     // Step 5: Save the updated array back to localStorage
//   //     localStorage.setItem("viewedProducts", JSON.stringify(viewedProducts));
//   //   }
//   // };
//   const handleProductClick = (product) => {
//   // Step 1: Retrieve the previously viewed products from localStorage, or initialize an empty array if not found
//   let viewedProducts = JSON.parse(localStorage.getItem("viewedProducts")) || [];

//   // Step 2: Check if the clicked product already exists in the array
//   const isProductAlreadyViewed = viewedProducts.some(p => p.id === product.id);

//   // Step 3: If the product hasn't been viewed already, add it to the array
//   if (!isProductAlreadyViewed) {
//     // Add the new product to the list
//     viewedProducts.push(product);

//     // Step 4: Limit the array to the last 5 viewed products
//     if (viewedProducts.length > 5) {
//       // If there are more than 5 products, remove the oldest (first in the array)
//       viewedProducts.shift();
//     }

//     // Step 5: Save the updated array back to localStorage
//     localStorage.setItem("viewedProducts", JSON.stringify(viewedProducts));
//   }
// };


//   if (loading) {
//     return (
//       <div className="flex justify-center items-center min-h-screen">
//         <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
//       </div>
//     );
//   }

//   if (error) {
//     return <div className="text-center text-red-500">Error: {error}</div>;
//   }

//   if (!products.length) {
//     return <div className="text-center text-lg">No products found.</div>;
//   }

//   return (
//     <div className="flex justify-center">
//       <div className="w-11/12">
//         {/* Sorting and Filtering Controls */}
//         <div className="mb-4 flex justify-between">
//           {/* Sort Dropdown */}
//           <select
//             value={sortOption}
//             onChange={(e) => handleSort(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="none">No Sorting</option>
//             <option value="price-asc">Price: Low to High</option>
//             <option value="price-desc">Price: High to Low</option>
//           </select>

//           {/* Filter Dropdown */}
//           <select
//             value={filterOption}
//             onChange={(e) => handleFilter(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="all">All Ratings</option>
//             <option value="high">High Ratings (4-5)</option>
//             <option value="normal">Normal Ratings (3-4)</option>
//             <option value="low">Low Ratings (1-3)</option>
//           </select>
//         </div>

//         {/* Product Grid */}
//         <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
//           {sortedProducts.map((product) => (
//             <a
//               key={product.id}
//               onClick={() => handleProductClick(product)} // Track the product click
//               target="_blank"
//               rel="noopener noreferrer"
//               href={product.link}
//               className="border rounded-lg p-4 flex flex-col items-center bg-white shadow-lg hover:shadow-xl transition"
//             >
//               {/* Product Image */}
//               <img
//                 src={product.image_url}
//                 alt={product.title}
//                 className="w-full h-40 object-contain mb-4"
//               />

//               {/* Product Title */}
//               <h2 className="text-md mb-2 text-left w-full whitespace-nowrap overflow-hidden text-ellipsis">
//                 {product.title}
//               </h2>

//               {/* Product Price */}
//               <p className="text-gray-700 font-bold mb-2">Rs {product.price}</p>

//               {/* Rating & Stars */}
//               <div className="flex items-center justify-between w-full text-sm">
//                 <div className="flex items-center">
//                   <span className="mr-1">★</span>
//                   <span className="font-semibold">
//                     {product.stars || "N/A"}
//                   </span>
//                   <span>/5</span>
//                   <span className="text-gray-600 ml-2">
//                     ({product.review_count || "0"} )
//                   </span>
//                 </div>
//                 <div className="bg-blue-500 text-white px-1 py-1 rounded-full text-xs font-semibold">
//                   {product.sentiment_score * 2 || "0"}/10
//                 </div>
//               </div>
//             </a>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ProductList;

// -==================================================================================till local storage

// import React, { useEffect, useState } from "react";

// const ProductList = ({ searchTerm }) => {
//   const [products, setProducts] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);
//   const [sortOption, setSortOption] = useState("none");
//   const [filterOption, setFilterOption] = useState("all");
//   const [viewedProducts, setViewedProducts] = useState([]);

//   useEffect(() => {
//     // Load viewed products from localStorage initially
//     const savedViewedProducts = JSON.parse(localStorage.getItem("viewedProducts")) || [];
//     setViewedProducts(savedViewedProducts);

//     // Fetch products based on searchTerm
//     const fetchProducts = async () => {
//       if (!searchTerm) return;

//       setLoading(true);
//       setError(null);

//       try {
//         const response = await fetch(
//           `http://localhost:8000/api/search?query=${searchTerm}`
//         );

//         if (!response.ok) {
//           throw new Error("Failed to fetch products.");
//         }

//         const result = await response.json();

//         if (result.success) {
//           setProducts(result.data);
//         } else {
//           throw new Error(result.message || "Failed to fetch products.");
//         }
//       } catch (err) {
//         setError(err.message);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchProducts();
//   }, [searchTerm]);

//   const handleSort = (option) => {
//     setSortOption(option);
//   };

//   const handleFilter = (option) => {
//     setFilterOption(option);
//   };
// const handleProductClick = (product) => {
//   // Step 1: Retrieve the previously viewed products from localStorage, or initialize an empty array if not found
//   let viewedProducts = JSON.parse(localStorage.getItem("viewedProducts")) || [];

//   // Step 2: Check if the clicked product already exists in the array by checking the _id
//   const isProductAlreadyViewed = viewedProducts.some(p => p._id === product._id);

//   // Step 3: If the product hasn't been viewed already, add it to the array
//   if (!isProductAlreadyViewed) {
//     // Add the new product to the list
//     viewedProducts.push(product);

//     // Step 4: Limit the array to the last 5 viewed products
//     if (viewedProducts.length > 5) {
//       viewedProducts.shift();  // Remove the oldest product
//     }

//     // Step 5: Save the updated array back to localStorage
//     localStorage.setItem("viewedProducts", JSON.stringify(viewedProducts));

//     // Optionally, update the React state to trigger a re-render if you need to use it elsewhere
//     setViewedProducts(viewedProducts);
//   }
// };


//   const sortedProducts = (() => {
//     let filteredProducts = [...products];

//     if (filterOption === "high") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 4
//       );
//     } else if (filterOption === "normal") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 3 && product.stars < 4
//       );
//     } else if (filterOption === "low") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 1 && product.stars < 3
//       );
//     }

//     if (sortOption === "price-asc") {
//       return filteredProducts.sort((a, b) => a.price - b.price);
//     } else if (sortOption === "price-desc") {
//       return filteredProducts.sort((a, b) => b.price - a.price);
//     }

//     return filteredProducts;
//   })();

//   if (loading) {
//     return (
//       <div className="flex justify-center items-center min-h-screen">
//         <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
//       </div>
//     );
//   }

//   if (error) {
//     return <div className="text-center text-red-500">Error: {error}</div>;
//   }

//   if (!products.length) {
//     return <div className="text-center text-lg">No products found.</div>;
//   }

//   return (
//     <div className="flex justify-center">
//       <div className="w-11/12">
//         {/* Sorting and Filtering Controls */}
//         <div className="mb-4 flex justify-between">
//           {/* Sort Dropdown */}
//           <select
//             value={sortOption}
//             onChange={(e) => handleSort(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="none">No Sorting</option>
//             <option value="price-asc">Price: Low to High</option>
//             <option value="price-desc">Price: High to Low</option>
//           </select>

//           {/* Filter Dropdown */}
//           <select
//             value={filterOption}
//             onChange={(e) => handleFilter(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="all">All Ratings</option>
//             <option value="high">High Ratings (4-5)</option>
//             <option value="normal">Normal Ratings (3-4)</option>
//             <option value="low">Low Ratings (1-3)</option>
//           </select>
//         </div>

//         {/* Product Grid */}
//         <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
//           {sortedProducts.map((product) => (
//             <a
//               key={product.id}
//               onClick={() => handleProductClick(product)} // Track the product click
//               target="_blank"
//               rel="noopener noreferrer"
//               href={product.link}
//               className="border rounded-lg p-4 flex flex-col items-center bg-white shadow-lg hover:shadow-xl transition"
//             >
//               {/* Product Image */}
//               <img
//                 src={product.image_url}
//                 alt={product.title}
//                 className="w-full h-40 object-contain mb-4"
//               />

//               {/* Product Title */}
//               <h2 className="text-md mb-2 text-left w-full whitespace-nowrap overflow-hidden text-ellipsis">
//                 {product.title}
//               </h2>

//               {/* Product Price */}
//               <p className="text-gray-700 font-bold mb-2">Rs {product.price}</p>

//               {/* Rating & Stars */}
//               <div className="flex items-center justify-between w-full text-sm">
//                 <div className="flex items-center">
//                   <span className="mr-1">★</span>
//                   <span className="font-semibold">
//                     {product.stars || "N/A"}
//                   </span>
//                   <span>/5</span>
//                   <span className="text-gray-600 ml-2">
//                     ({product.review_count || "0"} )
//                   </span>
//                 </div>
//                 <div className="bg-blue-500 text-white px-1 py-1 rounded-full text-xs font-semibold">
//                   {product.sentiment_score * 2 || "0"}/10
//                 </div>
//               </div>
//             </a>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ProductList;
// ============================================================================================
// import React, { useState, useEffect } from "react";

// const ProductList = ({ searchTerm, results, recommendedProducts }) => {
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);
//   const [sortOption, setSortOption] = useState("none");
//   const [filterOption, setFilterOption] = useState("all");
//   const [products, setProducts] = useState([]);

//   useEffect(() => {
//     if (recommendedProducts && recommendedProducts.length > 0) {
//       // If recommendations are passed, use them as products
//       setProducts(recommendedProducts);
//     } else if (searchTerm) {
//       // If a search term is provided, fetch products using the search term
//       fetchProductsBySearchTerm(searchTerm);
//     }
//   }, [searchTerm, recommendedProducts]);

//   const fetchProductsBySearchTerm = async (searchTerm) => {
//     setLoading(true);
//     setError(null);
//     try {
//       const response = await fetch(`http://localhost:5000/api/search?query=${searchTerm}`);
//       if (!response.ok) {
//         throw new Error("Failed to fetch products.");
//       }
//       const result = await response.json();
//       if (result.success) {
//         setProducts(result.data);
//       } else {
//         throw new Error(result.message || "Failed to fetch products.");
//       }
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleSort = (option) => {
//     setSortOption(option);
//   };

//   const handleFilter = (option) => {
//     setFilterOption(option);
//   };

//   const sortedProducts = (() => {
//     let filteredProducts = [...products];

//     if (filterOption === "high") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 4
//       );
//     } else if (filterOption === "normal") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 3 && product.stars < 4
//       );
//     } else if (filterOption === "low") {
//       filteredProducts = filteredProducts.filter(
//         (product) => product.stars >= 1 && product.stars < 3
//       );
//     }

//     if (sortOption === "price-asc") {
//       return filteredProducts.sort((a, b) => a.price - b.price);
//     } else if (sortOption === "price-desc") {
//       return filteredProducts.sort((a, b) => b.price - a.price);
//     }

//     return filteredProducts;
//   })();

//   const handleProductClick = (product) => {
//     let viewedProducts = JSON.parse(localStorage.getItem("viewedProducts")) || [];

//     const isProductAlreadyViewed = viewedProducts.some(p => p._id === product._id);

//     if (!isProductAlreadyViewed) {
//       viewedProducts.push(product);
//       if (viewedProducts.length > 5) viewedProducts.shift();
//       localStorage.setItem("viewedProducts", JSON.stringify(viewedProducts));
//     }
//   };

//   if (loading) {
//     return (
//       <div className="flex justify-center items-center min-h-screen">
//         <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
//       </div>
//     );
//   }

//   if (error) {
//     return <div className="text-center text-red-500">Error: {error}</div>;
//   }

//   if (!products.length) {
//     return <div className="text-center text-lg">No products found.</div>;
//   }

//   return (
//     <div className="flex justify-center">
//       <div className="w-11/12">
//         {/* Sorting and Filtering Controls */}
//         <div className="mb-4 flex justify-between">
//           <select value={sortOption} onChange={(e) => handleSort(e.target.value)} className="border p-2 rounded-md">
//             <option value="none">No Sorting</option>
//             <option value="price-asc">Price: Low to High</option>
//             <option value="price-desc">Price: High to Low</option>
//           </select>

//           <select value={filterOption} onChange={(e) => handleFilter(e.target.value)} className="border p-2 rounded-md">
//             <option value="all">All Ratings</option>
//             <option value="high">High Ratings (4-5)</option>
//             <option value="normal">Normal Ratings (3-4)</option>
//             <option value="low">Low Ratings (1-3)</option>
//           </select>
//         </div>

//         {/* Product Grid */}
//         <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
//           {sortedProducts.map((product) => (
//             <a
//               key={product.id}
//               onClick={() => handleProductClick(product)} // Track the product click
//               target="_blank"
//               rel="noopener noreferrer"
//               href={product.link}
//               className="border rounded-lg p-4 flex flex-col items-center bg-white shadow-lg hover:shadow-xl transition"
//             >
//               <img
//                 src={product.image_url}
//                 alt={product.title}
//                 className="w-full h-40 object-contain mb-4"
//               />
//               <h2 className="text-md mb-2 text-left w-full whitespace-nowrap overflow-hidden text-ellipsis">
//                 {product.title}
//               </h2>
//               <p className="text-gray-700 font-bold mb-2">Rs {product.price}</p>
//               <div className="flex items-center justify-between w-full text-sm">
//                 <div className="flex items-center">
//                   <span className="mr-1">★</span>
//                   <span className="font-semibold">{product.stars || "N/A"}</span>
//                   <span>/5</span>
//                   <span className="text-gray-600 ml-2">({product.review_count || "0"})</span>
//                 </div>
//                 <div className="bg-blue-500 text-white px-1 py-1 rounded-full text-xs font-semibold">
//                   {product.sentiment_score * 2 || "0"}/10
//                 </div>
//               </div>
//             </a>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ProductList;




import React, { useState, useEffect } from "react";

const ProductList = ({ results }) => {
  // const [sortOption, setSortOption] = useState("none");
  const [filterOption, setFilterOption] = useState("all");
  const [products, setProducts] = useState([]);
  const [sentimentSortOption, setSentimentSortOption] = useState("sentiment-high");
  const [priceSortOption, setPriceSortOption] = useState("none");

  useEffect(() => {
    setProducts(Array.isArray(results) ? results : []);
  }, [results]);

  const handleProductClick = (product) => {
    const viewed = JSON.parse(localStorage.getItem("viewedProducts")) || [];
    
    if (!viewed.some(p => p._id === product._id)) {
      const updated = [product, ...viewed].slice(0, 5);
      localStorage.setItem("viewedProducts", JSON.stringify(updated));
    }
  };

   // Helper function to parse price and remove currency symbols
//   const parsePrice = (price) => {
//   if (!price) return 0;
  
//   // Handle cases where price is already a number
//   if (typeof price === 'number') return price;
  
//   // Extract the numeric part of the price string
//   const numericPart = price.replace(/[^\d.,]/g, '');
  
//   // Handle commas and different decimal formats
//   const cleanPrice = numericPart
//     .replace(/\./g, '')   // Remove thousands separators (periods)
//     .replace(/,/g, '.')   // Replace commas with decimal points
//     .replace(/[^\d.]/g, ''); // Remove any remaining non-digit/non-period characters

//   return parseFloat(cleanPrice) || 0;
// };
// Helper function to parse price and remove currency symbols
const parsePrice = (price) => {
  if (!price) return 0;

  // Handle cases where price is already a number
  if (typeof price === 'number') return price;

  // Remove any currency symbols (like $, €, etc.) and trim the string
  const cleanedPrice = price.replace(/[^\d.,]/g, '').trim();

  // Remove commas and treat period as decimal separator
  const numericPart = cleanedPrice.replace(/,/g, ''); // Remove all commas
  
  // Replace the last period (if exists) with a decimal point and convert to float
  const cleanPrice = numericPart.replace(/\.(?=.*\.)/, ''); // Keeps only the last period as decimal

  return parseFloat(cleanPrice) || 0;
};


  const processedProducts = () => {
    let filtered = [...products];
    
    // Filtering logic from second code
    if (filterOption === "high") {
      filtered = filtered.filter(p => p.stars >= 4);
    } else if (filterOption === "normal") {
      filtered = filtered.filter(p => p.stars >= 3 && p.stars < 4);
    } else if (filterOption === "low") {
      filtered = filtered.filter(p => p.stars < 3);
    }
    
     // Sorting by price (numeric)
    // if (priceSortOption === "price-asc") {
    //   filtered = filtered.sort((a, b) => parsePrice(a.price) - parsePrice(b.price)); // Parse price to number
    // } else if (priceSortOption === "price-desc") {
    //   filtered = filtered.sort((a, b) => parsePrice(b.price) - parsePrice(a.price)); // Parse price to number
    // }
     // Sorting by price (numeric)
  if (priceSortOption === "price-asc") {
    filtered = filtered.sort((a, b) => 
      parsePrice(a.price) - parsePrice(b.price)
    );
  } else if (priceSortOption === "price-desc") {
    filtered = filtered.sort((a, b) => 
      parsePrice(b.price) - parsePrice(a.price)
    );
  }

    // Sorting by sentiment
    if (sentimentSortOption === "sentiment-high") {
      filtered = filtered.sort((a, b) => (b.sentiment_score || 0) - (a.sentiment_score || 0)); // High sentiment score first
    } else if (sentimentSortOption === "sentiment-low") {
      filtered = filtered.sort((a, b) => (a.sentiment_score || 0) - (b.sentiment_score || 0)); // Low sentiment score first
    }
    
    return filtered;
  };

  const finalProducts = processedProducts();

  if (!finalProducts.length) {
    return <div className="text-center text-lg py-8">No products found</div>;
  }

  return (
    <div className="flex justify-center">
      <div className="w-11/12">
        {/* Sorting and Filtering Controls - Design from first code */}
        <div className="mb-4 flex justify-between">
          {/* Price Sorting Dropdown */}
          <div>
            <select
              value={priceSortOption}
              onChange={(e) => setPriceSortOption(e.target.value)}
              className="border p-2 rounded-md"
            >
              <option value="none">Price Sorting</option>
              <option value="price-asc">Price: Low to High</option>
              <option value="price-desc">Price: High to Low</option>
            </select>
          </div>
          {/* Sentiment Sorting Dropdown */}
          <div>
            <select
              value={sentimentSortOption}
              onChange={(e) => setSentimentSortOption(e.target.value)}
              className="border p-2 rounded-md"
            >
              <option value="none">Sentiment Sorting</option>
              <option value="sentiment-high">Sentiment: High to Low</option>
              <option value="sentiment-low">Sentiment: Low to High</option>
            </select>
          </div>

          {/* Filter Dropdown */}
          <select
            value={filterOption}
            onChange={(e) => setFilterOption(e.target.value)}
            className="border p-2 rounded-md"
          >
            <option value="all">All Ratings</option>
            <option value="high">High Ratings (4-5)</option>
            <option value="normal">Normal Ratings (3-4)</option>
            <option value="low">Low Ratings (1-3)</option>
          </select>
        </div>

        {/* Product Grid - Design from first code */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
          {finalProducts.map((product) => (
            <a
              key={product._id}
              onClick={() => handleProductClick(product)}
              target="_blank"
              rel="noopener noreferrer"
              href={product.link}
              className="relative border rounded-lg p-4 flex flex-col items-center bg-white shadow-lg hover:shadow-xl transition"
            >
               {/* Conditionally render "Recommended" Badge */}
              {product.sentiment_score > 4.2 && (
                <div className="absolute top-2 left-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">
                  Recommended
                </div>
              )}
              {/* Product Image */}
              <img
                src={product.image_url}
                alt={product.title}
                className="w-full h-40 object-contain mb-4"
              />

              {/* Product Title */}
              <h2 className="text-md  text-left w-full line-clamp-2 h-12">
                {product.title}
              </h2>

              {/* Product Price */}
              <p className="text-gray-700 font-bold mb-2"> {product.price}</p>

              {/* Rating & Stars */}
              <div className="flex items-center justify-between w-full text-sm">
                <div className="flex items-center">
                  <span className="mr-1">★</span>
                  <span className="font-semibold">
                  {product.stars ? parseFloat(product.stars).toFixed(1) : "N/A"}
 
                  </span>
                  <span>/5</span>
                  <span className="text-gray-600 ml-2">
                    ({product.review_count || "0"})
                  </span>
                </div>
                <div className="bg-blue-500 text-white px-1 py-1 rounded-full text-xs font-semibold">
                  {product.sentiment_score ? (product.sentiment_score * 2).toFixed(1) : "0"}/10
                </div>
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProductList;