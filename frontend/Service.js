import baseURL from "./BaseURL.js";

export const service = {
  getLastUpdate: async () => {
    const response = await baseURL.get("/last_update");
    return response.data;
  },

  openWB: async () => {
    const response = await baseURL.post("/open_wb");
    return response.data;
  },

  saveWB: async () => {
    const response = await baseURL.post("/save_wb");
    return response.data;
  },

  transactions: async (formData) => {
    const response = await baseURL.post("/transaction", formData);
    return response.data;
  },

  updateBetaSheet: async () => {
    const response = await baseURL.post("/beta_sheet");
    return response.data;
  },

  updateLedger: async (formData) => {
    const response = await baseURL.post("/ledger", formData);
    return response.data;
  },

  //changed post to put
  updateLog: async () => {
    const response = await baseURL.put("/log");
    return response.data;
  },

  updatePortfolio: async () => {
    const response = await baseURL.put("/update_portfolio");
    return response.data;
  },

  updateSheets: async () => {
    const response = await baseURL.put("/sheets");
    return response.data;
  },
};
