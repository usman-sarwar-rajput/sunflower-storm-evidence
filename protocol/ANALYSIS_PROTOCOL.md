# Historical case analysis

The event date is 2016-08-19 at the USDA Limited Irrigation Research Farm near Greeley, Colorado. The crop log and methodology establish hail at the field; the exact onset time is unavailable. All joins use local dates. Other storms cannot be excluded just because the field notes do not mention them.

The three-period windows are days −3 to −1, 0, and +1 to +3. The five-period windows are −14 to −8, −7 to −1, 0, +1 to +7, and +8 to +24. They are descriptive and were defined for this retrospective release. A phase mean equally weights observed date means; rainfall is totaled across all calendar days when complete. Missing canopy remains blank. There is no interpolation or carry-forward.

The paired hail comparison uses the same source plot on 18 and 23 August. Canopy is a green pixel fraction multiplied by 100. Each original value and date is checked by its physical CSV line. The season comparison ranks the matched mean against all consecutive 2016 sampled date intervals. Gaps and crop stages vary, so this rank is not a calibrated p-value or a comparison against verified storm-free periods.

The direct inclination analysis subtracts the source linear-model angle from the trigonometric estimate on each record. Signed mean, mean absolute difference, sample standard deviation and RMSE are descriptive. No reference angle is designated as ground truth. The stem analysis uses complete observations on source time indices 14 through 77 and differences across one-hour intervals.

# Prospective head orientation study

1. Observe young and mature plants separately. Track the outward head axis and the upper stem independently, using synchronized calibrated imagery and fixed site references. Validate observed angles with known physical targets and independent annotation. Record rain, wind, gusts, light, pressure, humidity, temperature and soil water.
2. Define plot storm onset and end from independent local instrumentation and radar before viewing plant traces. Keep separate timestamps for gust front, precipitation and severe conditions. Use continuous recording, including calm, cloudy and gusty days without storms.
3. Compare the two hours before onset, the verified storm interval, two hours after and the next comparable solar times. Fit normal posture from storm-free periods by solar time and growth stage. Estimate the angular departure in degrees. Use circular or 3D geometry and account for repeated plants, time correlation and storm/site clustering. Estimate recovery against a predefined tolerance at matched solar time.
4. Predefine a forecast target, such as a site event within 15–60 minutes. Fit weather-only and weather-plus-plant models with time-available inputs. Separate development and evaluation by whole storm systems and preferably by site and season. Compute held-out lead time, sensitivity, false alarms per day and probability calibration. The number of storms, rather than the number of individual plant images, determines event-level replication.
5. If event-matched head observations or adequate independent storms are missing, keep the warning estimate unavailable. Source time indices from stem or inclination workbooks are not substitutes for actual event timestamps.

The three template CSVs are header-only and contain no simulated records.
