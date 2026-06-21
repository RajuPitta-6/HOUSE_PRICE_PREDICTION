const API_URL = "https://house-price-prediction-raz.onrender.com/predict";

const form = document.getElementById("prediction-form");
const predictBtn = document.getElementById("predict-btn");
const resultSection = document.getElementById("result-section");
const resultPrice = document.getElementById("result-price");
const errorSection = document.getElementById("error-section");
const errorMessage = document.getElementById("error-message");

const fields = {
  city: document.getElementById("city"),
  "locality-tier": document.getElementById("locality-tier"),
  bhk: document.getElementById("bhk"),
  bathrooms: document.getElementById("bathrooms"),
  "super-area": document.getElementById("super-area"),
  "property-age": document.getElementById("property-age"),
  parking: document.getElementById("parking"),
  furnishing: document.getElementById("furnishing"),
  distance: document.getElementById("distance"),
};

const validationRules = {
  city: {
    validate: (value) => value !== "",
    message: "Please select a city.",
  },
  "locality-tier": {
    validate: (value) => value !== "",
    message: "Please select a locality tier.",
  },
  bhk: {
    validate: (value) => Number.isInteger(Number(value)) && value >= 1 && value <= 10,
    message: "BHK must be a whole number between 1 and 10.",
  },
  bathrooms: {
    validate: (value) => Number.isInteger(Number(value)) && value >= 1 && value <= 10,
    message: "Bathrooms must be a whole number between 1 and 10.",
  },
  "super-area": {
    validate: (value) => !Number.isNaN(Number(value)) && Number(value) >= 100,
    message: "Super area must be at least 100 sqft.",
  },
  "property-age": {
    validate: (value) => Number.isInteger(Number(value)) && value >= 0 && value <= 100,
    message: "Property age must be between 0 and 100 years.",
  },
  parking: {
    validate: (value) => value === "0" || value === "1",
    message: "Please select parking availability.",
  },
  furnishing: {
    validate: (value) => value !== "",
    message: "Please select a furnishing type.",
  },
  distance: {
    validate: (value) => !Number.isNaN(Number(value)) && Number(value) >= 0,
    message: "Distance must be a valid number (0 or greater).",
  },
};

function showFieldError(fieldName, message) {
  const input = fields[fieldName];
  const errorEl = document.querySelector(`[data-error-for="${fieldName}"]`);

  if (input) {
    input.classList.add("invalid");
  }
  if (errorEl) {
    errorEl.textContent = message;
  }
}

function clearFieldError(fieldName) {
  const input = fields[fieldName];
  const errorEl = document.querySelector(`[data-error-for="${fieldName}"]`);

  if (input) {
    input.classList.remove("invalid");
  }
  if (errorEl) {
    errorEl.textContent = "";
  }
}

function validateField(fieldName) {
  const input = fields[fieldName];
  const rule = validationRules[fieldName];
  const value = input.type === "number" ? input.value.trim() : input.value;

  if (!rule.validate(value)) {
    showFieldError(fieldName, rule.message);
    return false;
  }

  clearFieldError(fieldName);
  return true;
}

function validateForm() {
  let isValid = true;

  Object.keys(validationRules).forEach((fieldName) => {
    if (!validateField(fieldName)) {
      isValid = false;
    }
  });

  return isValid;
}

function hideMessages() {
  resultSection.classList.add("hidden");
  errorSection.classList.add("hidden");
}

function showError(message) {
  hideMessages();
  errorMessage.textContent = message;
  errorSection.classList.remove("hidden");
  errorSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function showResult(price) {
  hideMessages();
  resultPrice.textContent = formatPrice(price);
  resultSection.classList.remove("hidden");
  resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function formatPrice(value) {
  const amount = Number(value);

  if (Number.isNaN(amount)) {
    return String(value);
  }

  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(amount);
}

function buildPayload() {
  return {
    City: fields.city.value,
    Locality_Tier: fields["locality-tier"].value,
    BHK: parseInt(fields.bhk.value, 10),
    Bathrooms: parseInt(fields.bathrooms.value, 10),
    Super_Area_sqft: parseFloat(fields["super-area"].value),
    Property_Age_years: parseInt(fields["property-age"].value, 10),
    Parking: parseInt(fields.parking.value, 10),
    Furnishing: fields.furnishing.value,
    Distance_to_CityCenter_km: parseFloat(fields.distance.value),
  };
}

function extractPrice(data) {
  if (typeof data === "number") {
    return data;
  }

  if (data && typeof data === "object") {
    return (
      data["preidicted price"] ??
      data.predicted_price ??
      data.predictedPrice ??
      data.price ??
      data.prediction
    );
  }

  return null;
}

function setLoading(isLoading) {
  predictBtn.disabled = isLoading;
  predictBtn.classList.toggle("loading", isLoading);
}

Object.keys(fields).forEach((fieldName) => {
  fields[fieldName].addEventListener("input", () => clearFieldError(fieldName));
  fields[fieldName].addEventListener("change", () => clearFieldError(fieldName));
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideMessages();

  if (!validateForm()) {
    showError("Please fix the highlighted fields before submitting.");
    return;
  }

  setLoading(true);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(buildPayload()),
    });

    if (!response.ok) {
      let detail = "Unable to get a prediction. Please try again.";
      try {
        const errorData = await response.json();
        detail = errorData.detail ?? errorData.message ?? detail;
        if (Array.isArray(detail)) {
          detail = detail.map((item) => item.msg ?? item).join(" ");
        }
      } catch {
        /* use default message */
      }
      throw new Error(detail);
    }

    const data = await response.json();
    const price = extractPrice(data);

    if (price === null || price === undefined) {
      throw new Error("Unexpected response from the server.");
    }

    showResult(price);
  } catch (error) {
    const message =
      error.message === "Failed to fetch"
        ? "Could not reach the API. Make sure the server is running at http://127.0.0.1:8000."
        : error.message;
    showError(message);
  } finally {
    setLoading(false);
  }
});
