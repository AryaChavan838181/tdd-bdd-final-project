"use strict";
const fields = ["id", "name", "description", "price", "available", "category"];
const el = name => document.getElementById("product_" + name);
const flash = msg => { document.getElementById("flash_message").textContent = msg; };
const formData = () => ({ name:el("name").value, description:el("description").value,
  price:el("price").value, available:el("available").value === "true",
  category:el("category").value || "UNKNOWN" });
const populate = product => {
  for (const k of fields) el(k).value = product[k] === null || product[k] === undefined ? "" : String(product[k]);
  el("available").value = String(product.available).toLowerCase();
};
function clearForm() { for (const k of fields) el(k).value = ""; flash(""); }
async function api(method, url, data) {
  const opts = { method, headers: data ? {"Content-Type":"application/json"} : {} };
  if (data) opts.body = JSON.stringify(data);
  const resp = await fetch(url, opts);
  const value = resp.status === 204 ? null : await resp.json().catch(() => null);
  if (!resp.ok) throw new Error((value && value.description) || `${resp.status}: request failed`);
  return value;
}
async function action(fn) { flash("Working..."); try { await fn(); } catch (e) { flash(e.message); } }
document.getElementById("clear-btn").addEventListener("click", clearForm);
document.getElementById("create-btn").addEventListener("click", () => action(async () => {
  const p = await api("POST", "/products", formData()); populate(p); flash("Success");
}));
document.getElementById("retrieve-btn").addEventListener("click", () => action(async () => {
  const p = await api("GET", "/products/" + el("id").value); populate(p); flash("Success");
}));
document.getElementById("update-btn").addEventListener("click", () => action(async () => {
  const p = await api("PUT", "/products/" + el("id").value, formData()); populate(p); flash("Success");
}));
document.getElementById("delete-btn").addEventListener("click", () => action(async () => {
  await api("DELETE", "/products/" + el("id").value); clearForm(); flash("Product has been Deleted!");
}));
document.getElementById("search-btn").addEventListener("click", () => action(async () => {
  const query = new URLSearchParams();
  if (el("name").value) query.set("name", el("name").value);
  else if (el("category").value) query.set("category", el("category").value);
  else if (el("available").value) query.set("available", el("available").value);
  const products = await api("GET", "/products" + (query.toString() ? "?" + query : ""));
  const body = document.getElementById("search_results"); body.replaceChildren();
  for (const p of products) {
    const tr = document.createElement("tr");
    for (const k of fields) { const td = document.createElement("td"); td.textContent = p[k]; tr.append(td); }
    tr.addEventListener("click", () => populate(p)); body.append(tr);
  }
  if (products.length) populate(products[0]);
  flash("Success");
}));
