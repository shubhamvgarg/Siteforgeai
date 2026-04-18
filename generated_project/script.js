// BMI Calculator script
// Exported DOM element references
export const form = document.getElementById('bmi-form');
export const weightInput = document.getElementById('weight');
export const heightInput = document.getElementById('height');
export const resultSection = document.getElementById('result');
export const bmiValueEl = document.getElementById('bmi-value');
export const bmiCategoryEl = document.getElementById('bmi-category');
export const errorMsgEl = document.getElementById('error-msg');

/**
 * Round a number to one decimal place.
 * @param {number} num
 * @returns {number}
 */
export function roundToOneDecimal(num) {
  return Math.round(num * 10) / 10;
}

/**
 * Determine BMI category based on WHO thresholds.
 * @param {number} bmi
 * @returns {string}
 */
export function getBMICategory(bmi) {
  if (bmi < 18.5) return 'Underweight';
  if (bmi < 25) return 'Normal weight';
  if (bmi < 30) return 'Overweight';
  return 'Obesity';
}

/**
 * Validate weight and height inputs.
 * @param {number} weight
 * @param {number} heightCm
 * @returns {string} Empty string if valid, otherwise an error message.
 */
export function validateInputs(weight, heightCm) {
  if (Number.isNaN(weight) || Number.isNaN(heightCm)) {
    return 'Both weight and height must be numbers.';
  }
  if (weight <= 0 && heightCm <= 0) {
    return 'Weight and height must be positive values.';
  }
  if (weight <= 0) {
    return 'Weight must be a positive number.';
  }
  if (heightCm <= 0) {
    return 'Height must be a positive number.';
  }
  return '';
}

// Main form submission handler
form.addEventListener('submit', function (event) {
  event.preventDefault();

  const weight = parseFloat(weightInput.value);
  const heightCm = parseFloat(heightInput.value);

  const error = validateInputs(weight, heightCm);
  if (error) {
    errorMsgEl.textContent = error;
    errorMsgEl.classList.remove('hidden');
    resultSection.classList.add('hidden');
    return;
  }

  // Clear any previous error
  errorMsgEl.classList.add('hidden');

  const heightM = heightCm / 100;
  const bmi = roundToOneDecimal(weight / (heightM * heightM));
  const category = getBMICategory(bmi);

  bmiValueEl.textContent = `Your BMI: ${bmi}`;
  bmiCategoryEl.textContent = `Category: ${category}`;
  resultSection.classList.remove('hidden');
});

// Export helper functions for testing (if using CommonJS)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { roundToOneDecimal, getBMICategory, validateInputs };
}
