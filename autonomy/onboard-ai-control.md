# Onboard AI & Control

State estimation, perception, planning, control and command authority are separate responsibilities. Neural inference can support perception; classical estimation, geometry and control do not universally require a neural network.

## Health is not permission

A navigation uncertainty value alone cannot authorize autonomy. The former table permitting full autonomy below a universal 5 m sigma is withdrawn. A reported covariance may be stale, inconsistent or expressed in a different frame; it also says nothing by itself about clearance, speed, command ownership or the aircraft's validated operating envelope.

| Input | What an integration must establish |
|---|---|
| Position/velocity | Reference frame, sample age, validity, uncertainty and estimator integrity |
| Environment | Observation coverage, clearance and missing/stale-data behavior |
| Control | Exact firmware mode prerequisites and supported setpoint/frame semantics |
| Authority | Current command owner, operator override and bounded action contract |
| Degradation | Documented behavior for invalid estimates, lost links and failed components |

For PX4 **v1.17**, Offboard mode requires a continuing proof-of-life stream and documented entry/loss conditions. Those firmware requirements do not establish application safety. [PX4 v1.17 Offboard documentation](https://docs.px4.io/v1.17/en/flight_modes/offboard), checked 2026-10-07.

## Software verification

Exercise stale samples, clock jumps, frame mismatch, sensor disagreement, disconnect/reconnect and operator revocation in simulation or replay. Log the input, decision, owner and resulting state transition. Passing a software test establishes that tested contract; hardware integration and field acceptance remain separate evidence categories.

See [software failure testing](../integration/software-failure-testing.md), [time and coordinates](../integration/time-and-coordinate-provenance.md), [telemetry ownership](../integration/secure-multiclient-telemetry.md) and [workload selection](../integration/compute-workload-selection.md).
