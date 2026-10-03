import { useState } from "react";

const companies = [
  "Dell", "Lenovo", "HP", "Asus", "Acer",
  "MSI", "Apple", "Toshiba", "Samsung",
  "Microsoft", "Razer", "LG", "Huawei", "Google"
];

const types = [
  "Notebook",
  "Ultrabook",
  "Gaming",
  "2 in 1 Convertible",
  "Workstation",
  "Netbook"
];

const cpus = [
  "Intel Core i3",
  "Intel Core i5",
  "Intel Core i7",
  "Intel Core i9",
  "AMD Ryzen 3",
  "AMD Ryzen 5",
  "AMD Ryzen 7",
  "AMD Ryzen 9",
  "Intel Core M",
  "Other Intel Processor",
  "AMD Processor"
];

const gpus = [
  "Intel",
  "Nvidia",
  "AMD",
  "ARM"
];

const operatingSystems = [
  "Windows",
  "Mac",
  "Linux",
  "Others"
];

const resolutions = [
  "1920x1080",
  "1366x768",
  "1600x900",
  "3840x2160",
  "3200x1800",
  "2880x1800",
  "2560x1600",
  "2560x1440",
  "2304x1440"
];

function App() {
  const [form, setForm] = useState({
    company: "Dell",
    type: "Notebook",
    ram: 16,
    weight: 1.6,
    touchscreen: "No",
    ips: "Yes",
    screen_size: 15.6,
    resolution: "1920x1080",
    cpu: "Intel Core i5",
    hdd: 0,
    ssd: 512,
    gpu: "Intel",
    os: "Windows"
  });

  const [price, setPrice] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm({
      ...form,
      [name]: ["ram", "hdd", "ssd"].includes(name)
        ? Number(value)
        : ["weight", "screen_size"].includes(name)
        ? Number(value)
        : value
    });
  };

  const predictPrice = async () => {
    setLoading(true);
    setPrice(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
      });

      const data = await response.json();

      setPrice(data.predicted_price);
    } catch (error) {
      alert("Backend is not running.");
    }

    setLoading(false);
  };

  return (
    <div className="container">

      <h1>Laptop Price Predictor</h1>

      <div className="grid">

        <label>
          Brand
          <select name="company" value={form.company} onChange={handleChange}>
            {companies.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>

        <label>
          Type
          <select name="type" value={form.type} onChange={handleChange}>
            {types.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>

        <label>
          RAM: {form.ram} GB
          <input
            type="range"
            name="ram"
            min="2"
            max="64"
            step="2"
            value={form.ram}
            onChange={handleChange}
          />
        </label>

        <label>
          Weight: {form.weight} kg
          <input
            type="number"
            name="weight"
            step="0.01"
            value={form.weight}
            onChange={handleChange}
          />
        </label>

        <label>
          Touchscreen
          <select
            name="touchscreen"
            value={form.touchscreen}
            onChange={handleChange}
          >
            <option>No</option>
            <option>Yes</option>
          </select>
        </label>

        <label>
          IPS
          <select name="ips" value={form.ips} onChange={handleChange}>
            <option>No</option>
            <option>Yes</option>
          </select>
        </label>

        <label>
          Screen Size: {form.screen_size}"
          <input
            type="range"
            name="screen_size"
            min="10"
            max="18"
            step="0.1"
            value={form.screen_size}
            onChange={handleChange}
          />
        </label>

        <label>
          Resolution
          <select
            name="resolution"
            value={form.resolution}
            onChange={handleChange}
          >
            {resolutions.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>

        <label>
          CPU
          <select name="cpu" value={form.cpu} onChange={handleChange}>
            {cpus.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>

        <label>
          HDD
          <select name="hdd" value={form.hdd} onChange={handleChange}>
            {[0, 128, 256, 512, 1024, 2048].map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>

        <label>
          SSD
          <select name="ssd" value={form.ssd} onChange={handleChange}>
            {[0, 8, 128, 256, 512, 1024].map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>

        <label>
          GPU
          <select name="gpu" value={form.gpu} onChange={handleChange}>
            {gpus.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>

        <label>
          OS
          <select name="os" value={form.os} onChange={handleChange}>
            {operatingSystems.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>

      </div>

      <button onClick={predictPrice} disabled={loading}>
        {loading ? "Predicting..." : "Predict Price"}
      </button>

      {price !== null && (
        <div className="result">
          Predicted Price: ₹{price.toLocaleString("en-IN")}
        </div>
      )}

    </div>
  );
}

export default App;