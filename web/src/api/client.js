const API_BASE = "http://localhost:8000/api/v1";

export const getAuthToken = () => localStorage.getItem("openmcp_token");
export const setAuthToken = (token) => localStorage.setItem("openmcp_token", token);
export const removeAuthToken = () => localStorage.removeItem("openmcp_token");

const request = async (endpoint, options = {}) => {
  const token = getAuthToken();
  const headers = {
    ...options.headers,
  };
  
  // Only set Content-Type to JSON if we are not sending FormData (which needs boundary generated automatically)
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errMessage = "An error occurred";
    try {
      const errorData = await response.json();
      errMessage = errorData.detail || errMessage;
    } catch(e) {}
    throw new Error(errMessage);
  }

  return response.json();
};

export const api = {
  login: async (username, password) => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);
    
    return fetch(`${API_BASE}/auth/login/access-token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    }).then(async (res) => {
      if (!res.ok) throw new Error("Login failed");
      return res.json();
    });
  },
  
  getMe: () => request("/users/me"),
  
  searchPackages: (query = "") => request(`/packages?q=${encodeURIComponent(query)}`),
  
  getPackage: (name) => request(`/packages/${name}`),
};
