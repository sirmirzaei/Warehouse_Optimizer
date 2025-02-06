const displayOrderTemplateLink = async () => {
    try {
        const response = await fetch("backend/process_customer_orders.php");
        const result = await response.json();

        if (result.status === "success" && document.getElementById("step3").style.display !== "none") {
            console.log("Displaying Order Template:", result.template_url);

            const downloadLink = document.createElement("a");
            downloadLink.href = "backend/" + result.template_url;
            downloadLink.innerText = "Download Order Template";
            downloadLink.className = "download-link";
            downloadLink.download = "order_template.xlsx";

            const templateDownloadDiv = document.getElementById("templateDownloadContainer");
            if (templateDownloadDiv) {
                templateDownloadDiv.innerHTML = "";
                templateDownloadDiv.appendChild(downloadLink);
            } else {
                console.error("Element with id 'templateDownloadContainer' not found in DOM.");
            }
        }
    } catch (error) {
        console.error("Error generating order template:", error);
    }
};


document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");
});


const displayLayoutTemplateLink = (templatePath) => {
    console.log("Displaying Layout Template:", templatePath);

    const filePath = templatePath.startsWith("http") ? templatePath : "backend/" + templatePath;

    const excelLink = document.createElement("a");
    excelLink.href = filePath;
    excelLink.innerText = "Download Layout Template";
    excelLink.className = "btn-link";
    excelLink.download = "template.xlsx";
    excelLink.style.display = "block";

    const templateDownloadDiv = document.getElementById("templateDownload");
    if (templateDownloadDiv) {
        templateDownloadDiv.innerHTML = "";
        templateDownloadDiv.appendChild(excelLink);
    } else {
        console.error("Element with id 'templateDownload' not found in DOM.");
    }
};


document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();



    const formData = new FormData();
    const fileInput = document.getElementById("warehouseMap");
    const scaleInput = document.getElementById("scale");
    const submitButton = document.querySelector("#uploadForm button[type='submit']");

    if (!fileInput.files.length || !scaleInput.value) {
        alert("Please upload the map and define the scale.");
        return;
    }

    formData.append("warehouseMap", fileInput.files[0]);
    formData.append("scale", scaleInput.value);

    try {
        const response = await fetch("backend/upload.php", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        console.log("Parsed Response:", result);

        if (result.status === "success") {
            document.getElementById("result").innerHTML = result.message;

            const resultContainer = document.getElementById("result");
            let lastElement = null; 



            
            if (result.annotated_plan) {
                const imgElement = document.createElement("img");
                imgElement.src = result.annotated_plan.startsWith("http") 
                    ? result.annotated_plan 
                    : "backend/" + result.annotated_plan;
                imgElement.alt = "Annotated Warehouse Map";
                imgElement.style.maxWidth = "100%";

                resultContainer.appendChild(document.createElement("br")); 
                resultContainer.appendChild(imgElement);
                lastElement = imgElement;
            }
            
            if (result.grid_data) {
                const jsonLink = document.createElement("a");
                jsonLink.href = result.grid_data.startsWith("http") 
                    ? result.grid_data 
                    : "backend/" + result.grid_data;
                jsonLink.innerText = "Download Grid Data (JSON)";
                jsonLink.className = "btn-link";
                jsonLink.download = "grid_data.json";
                resultContainer.appendChild(jsonLink);
                lastElement = jsonLink;
            }
            if (result.annotated_plan) {
                const imgDownloadLink = document.createElement("a");
                imgDownloadLink.href = result.annotated_plan.startsWith("http") 
                    ? result.annotated_plan 
                    : "backend/" + result.annotated_plan;
                imgDownloadLink.innerText = "Download Annotated Map";
                imgDownloadLink.className = "btn-link";
                imgDownloadLink.download = "annotated_plan.png";
                imgDownloadLink.style.display = "block"; 
            
                
                if (lastElement) {
                    lastElement.insertAdjacentElement("afterend", document.createElement("br"));
                    lastElement.insertAdjacentElement("afterend", imgDownloadLink);
                } else {
                    resultContainer.appendChild(document.createElement("br"));
                    resultContainer.appendChild(imgDownloadLink);
                }
            }
            

            submitButton.disabled = true;
            document.getElementById("step2").style.display = "block";

            if (result.template_excel) {
                displayLayoutTemplateLink(result.template_excel);
            }
        }
    } catch (error) {
        console.error("Error:", error);
    }
});




const handleExcelUpload = async (e) => {
    e.preventDefault();
    const labelElement = document.querySelector("label[for='productExcel']");
if (labelElement) {
    labelElement.remove();
}
    const formData = new FormData();
    const fileInput = document.getElementById("productExcel");
    const uploadButton = document.querySelector("#uploadExcelForm button[type='submit']");
    const formContainer = document.getElementById("uploadExcelForm").parentNode;

    if (!fileInput.files.length) {
        alert("Please upload the completed Excel file.");
        return;
    }

    formData.append("productExcel", fileInput.files[0]);

    try {
        const response = await fetch("backend/process_excel.php", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        console.log("Excel Upload Response:", result);

        if (result.status === "success") {
            document.getElementById("excelResult").innerHTML = result.message;

            
            uploadButton.style.display = "none";
            fileInput.style.display = "none";

            
            const oldConfirmationDiv = document.getElementById("confirmationOptions");
            if (oldConfirmationDiv) {
                oldConfirmationDiv.remove();
            }

            
            const confirmationDiv = document.createElement("div");
            confirmationDiv.id = "confirmationOptions";
            confirmationDiv.innerHTML = `
                <p>Do you want to continue with this file or upload a new one?</p>
                <button id="continueButton">Continue</button>
                <button id="reuploadButton">Upload New File</button>
            `;
            document.getElementById("excelResult").appendChild(confirmationDiv);

      
            document.getElementById("continueButton").addEventListener("click", async () => {
                document.getElementById("uploadExcelForm").style.display = "none";
                document.getElementById("confirmationOptions").remove();
            
                if (result.updated_image) {
                    const imgElement = document.createElement("img");
                    imgElement.src = "backend/" + result.updated_image;
                    imgElement.alt = "Updated Warehouse Map";
                    imgElement.style.maxWidth = "100%";
            
                    const downloadLink = document.createElement("a");
                    downloadLink.href = "backend/" + result.updated_image;
                    downloadLink.innerText = "Download Updated Map";
                    downloadLink.className = "download-link";
                    downloadLink.download = "annotated_plan_updated.png";
            
                    document.getElementById("updatedImageContainer").innerHTML = "";
                    document.getElementById("updatedImageContainer").append(imgElement, downloadLink);
                }
            
                
                document.getElementById("step3").style.display = "block";
            
                
                try {
                    const response = await fetch("backend/generate_customer_template.php", {
                        method: "POST"
                    });
            
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
            
                    const result = await response.json();
            
                    if (result.status === "success") {
                        
                        const customerTemplateLink = document.createElement("a");
                        customerTemplateLink.href = "backend/" + result.template_url;
                        customerTemplateLink.innerText = "Download Customer Order Template";
                        customerTemplateLink.className = "download-link";
                        customerTemplateLink.download = "order_template.xlsx";
            
                        
                        const step3Container = document.getElementById("step3");
                        const descriptionParagraph = step3Container.querySelector("p");
            
                        if (descriptionParagraph) {
                            descriptionParagraph.insertAdjacentElement("afterend", customerTemplateLink);
                        } else {
                            step3Container.prepend(customerTemplateLink);
                        }
                    } else {
                        console.error("Error generating customer template:", result.message, "Python Output:", result.output);
                    }
                } catch (error) {
                    console.error("Error generating customer template:", error);
                }
            });
            
            



            
            document.getElementById("reuploadButton").addEventListener("click", () => {
                
                const oldForm = document.getElementById("uploadExcelForm");
                if (oldForm) {
                    oldForm.remove();
                }

                
                const newForm = document.createElement("form");
                newForm.id = "uploadExcelForm";

                newForm.innerHTML = `
                    <div class="form-group">
                        <label for="productExcel">Upload Completed Excel File:</label>
                        <input type="file" id="productExcel" name="productExcel" accept=".xlsx, .xls" />
                    </div>
                    <button type="submit">Upload Excel</button>
                `;

                formContainer.appendChild(newForm);

                
                newForm.addEventListener("submit", handleExcelUpload);

                
                const confirmationDiv = document.getElementById("confirmationOptions");
                if (confirmationDiv) {
                    confirmationDiv.remove();
                }
            });
        }
    } catch (error) {
        console.error("Error:", error);
    }
};
document.getElementById("uploadCustomerOrderForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById("customerOrderFile");
    const uploadButton = document.querySelector("#uploadCustomerOrderForm button[type='submit']");
    const formContainer = document.getElementById("uploadCustomerOrderForm").parentNode;

    if (!fileInput.files.length) {
        alert("Please upload a customer order file.");
        return;
    }

    formData.append("customerOrderFile", fileInput.files[0]);

    try {
        
        const response = await fetch("backend/process_customer_orders.php", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        console.log("Customer Order Upload Response:", result);

        if (result.status === "success") {
            document.getElementById("customerOrderResult").innerHTML = result.message;

            
            uploadButton.style.display = "none";
            fileInput.style.display = "none";

            
            const oldConfirmationDiv = document.getElementById("customerConfirmationOptions");
            if (oldConfirmationDiv) {
                oldConfirmationDiv.remove();
            }

            
            const confirmationDiv = document.createElement("div");
            confirmationDiv.id = "customerConfirmationOptions";
            confirmationDiv.innerHTML = `
                <p>Do you want to continue with this file or upload a new one?</p>
                <button id="customerContinueButton">Continue</button>
                <button id="customerReuploadButton">Upload New File</button>
            `;
            document.getElementById("customerOrderResult").appendChild(confirmationDiv);

            document.getElementById("customerContinueButton").addEventListener("click", async () => {
                document.getElementById("customerConfirmationOptions").remove();
            
                try {
                    const response = await fetch("backend/process_customer_orders.php", {
                        method: "POST",
                        body: formData, 
                    });
            
                    const textResponse = await response.text();  // Read response as text first
                    console.log("Raw Response from PHP:", textResponse);
                    
                    try {
                        const result = JSON.parse(textResponse);
                        console.log("Parsed JSON Response:", result);
                    } catch (error) {
                        console.error("Error parsing JSON:", error, "Response was:", textResponse);
                    }
            
                    if (result.status === "success") {
                        document.getElementById("customerOrderResult").innerHTML = `
                            <p>${result.message}</p>
                            <p>Order Processing Completed Successfully!</p>
                        `;
            
                        
                        const analyzeResponse = await fetch("backend/analyze_orders.php", {
                            method: "POST",
                            body: JSON.stringify({ file_path: "uploads/customer_orders.xlsx" }),
                            headers: { "Content-Type": "application/json" }
                        });
            
                        const analyzeResult = await analyzeResponse.json();
                        console.log("Analysis Response:", analyzeResult);
            
                        if (analyzeResult.status === "success") {
                            document.getElementById("customerOrderResult").innerHTML += `
                                <p>Analysis Completed. <a href="backend/${analyzeResult.recommended_layout}" download>Download Optimized Excel</a></p>
                                <img src="backend/${analyzeResult.updated_image}" alt="Optimized Layout" style="max-width:100%;">
                            `;
                        } else {
                            document.getElementById("customerOrderResult").innerHTML += `<p>Error: ${analyzeResult.message}</p>`;
                        }
            
                    } else {
                        document.getElementById("customerOrderResult").innerHTML = `<p>Error Processing Order: ${result.message}</p>`;
                    }
                } catch (error) {
                    console.error("Error uploading customer order:", error);
                    document.getElementById("customerOrderResult").innerHTML = `<p>Unexpected error occurred. Please try again.</p>`;
                }
            });
            
            
            document.getElementById("customerReuploadButton").addEventListener("click", () => {
                
                const oldForm = document.getElementById("uploadCustomerOrderForm");
                if (oldForm) {
                    oldForm.remove();
                }

                
                const newForm = document.createElement("form");
                newForm.id = "uploadCustomerOrderForm";

                newForm.innerHTML = `
                    <div class="form-group">
                        <label for="customerOrderFile">Upload Customer Order File:</label>
                        <input type="file" id="customerOrderFile" name="customerOrderFile" accept=".xlsx, .xls" />
                    </div>
                    <button type="submit">Upload Order File</button>
                `;

                formContainer.appendChild(newForm);

                
                newForm.addEventListener("submit", async (event) => {
                    event.preventDefault();
                    document.getElementById("customerOrderResult").innerHTML = "";
                    handleCustomerOrderUpload(event);
                });

                
                const confirmationDiv = document.getElementById("customerConfirmationOptions");
                if (confirmationDiv) {
                    confirmationDiv.remove();
                }
            });
        }
    } catch (error) {
        console.error("Error processing customer order file:", error);
    }
});


document.getElementById("uploadExcelForm").addEventListener("submit", handleExcelUpload);