1. Configuration-Driven Architecture
All weights, limits, and policy constants are imported from rules.
Ensures separation of business logic and configuration.
Makes the system tunable without modifying core code.

2. Deterministic Rule Engine Design
Function takes structured context data (crops, soil, weather, prices, locations).
Stateless and testable: same input → same output.
Optional parameters (land_area, investment, seed_type) extend it to financial modeling.

3. Confidence-Based Scoring Model
Starts with INITIAL_CONFIDENCE.
Deducts weighted penalties for mismatches:
Soil
Rainfall
Temperature
Topography
Seasonal risks
Uses MIN_CONFIDENCE as lower bound to maintain score stability.
This creates an interpretable, modular risk scoring system.

4. Defensive Data Validation
Validates crop and district existence early.
Returns structured error instead of failing.
Prevents downstream crashes.

5. Environmental Compatibility Checks
Each factor is independently evaluated:
Soil compatibility
Rainfall suitability (handles multiple data formats)
Temperature band match
Topography suitability
Seasonal weather risks
Each mismatch reduces confidence and generates warnings/suggestions.

6. Yield Modeling (Multiplicative Adjustment)
Final yield is calculated as:
Base Yield × Seed Multiplier × Soil Fertility Modifier × Climate Modifier
Climate modifier = confidence / 100
This ties environmental suitability directly to productivity.
Production scales with land area.

7. Price Prediction
Uses weighted moving average of last 3 prices (0.5, 0.3, 0.2).
Captures short-term trends while smoothing volatility.
Lightweight alternative to time-series ML.

8. Financial Evaluation
Revenue = Production × Predicted Price
Net Value = Revenue − Investment
Classified as Profit / Loss / Break-even
Converts numeric output into actionable interpretation.

9. Policy Recommendation Engine
Rule-triggered suggestions based on:
High investment → subsidy
Low confidence → insurance
Seasonal risk → crop insurance
Low rainfall → irrigation scheme
Universal policies always included

Duplicates removed for clean output.
===============================================
Adjusted Yield = Base Yield
                 × Soil Fertility Modifier
                 × Seed Variety Multiplier
                 × Climate Confidence Modifier
                 
Total Production = Adjusted Yield × Land Area
Predicted Price = Weighted average of last N years (pre or post)
Revenue = Production × Price
Net = Revenue − Investment
