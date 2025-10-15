import axios from "axios";


const API_BASE_URL = "http://localhost:8000";

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
 
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    if (!(config.data instanceof FormData)) {
        config.headers["Content-Type"] = "application/json";
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const auth = {
  signup: async (userData) => axiosInstance.post("/auth/register", userData),
  signin: async (credentials) => {
    const response = await axiosInstance.post("/auth/login", credentials);
    localStorage.setItem("access_token", response.data.access_token);
    return response;
  },

  checkStatus: () => axiosInstance.get("/auth/me"),

  signout:() =>{
    localStorage.removeItem("access_token");
  },

 googleLogin: () => {
  window.location.href = "http://localhost:8000/auth/google/login";
}

};


export const jobService ={

    searchSkills: (jobTitle, city, state) =>{
        const formData = new FormData();
        formData.append("job_title", jobTitle);
        formData.append("city", city);
        formData.append("state", state);
        return axiosInstance.post("/jobmatch/skills", formData,{
            headers :{
                "Content-Type": "multipart/form-data"
            }

        });
    },

    getScore: (file) =>{
        const formData = new FormData();
        formData.append("file", file);
        
        return axiosInstance.post ("/jobmatch/analyze", formData,{});
    },
    
};