# فهرس صفحات موديول إدارة المرضى (Patient Management - BayMax)

تاريخ التحديث: 2026-11-07  
البيئة المستهدفة: `https://196.218.246.250:4040/home`  
التقنية: Angular 21 (SPA) + Bootstrap + PrimeNG (Cairo Font - RTL)  
قاعدة المعرفة المركزية الموحدة: [`KNOWLEDGE_BASE.json`](./KNOWLEDGE_BASE.json)

---

## 0. المكونات العامة وشريط التنقل (Global Components)
| # | المكون | المسار الأساسي | الفولدر | الحالة (Status) |
|---|---|---|---|---|
| 00 | شريط التنقل وقائمة مكتب الدخول (Top Navbar) | `/home` (Global) | [`00_navbar`](./00_navbar/) | ✅ Done |

---

## 1. قائمة مكتب الدخول (Admission / Reception) — (8 صفحات)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | عناصر `test-id` | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | الملف الطبى (بيانات المريض / دخول) | `/reception` | `<app-patient-data>` | [`01_reception_medical_file`](./01_reception_medical_file/) | 54 عنصر | ✅ Discovery Completed |
| 02 | تقرير إشغال المستشفى | `/reception/occupancy-report` | `<app-occupancy-report>` | [`02_reception_occupancy_report`](./02_reception_occupancy_report/) | 9 عناصر | ✅ Discovery Completed |
| 03 | تقرير الدخول والخروج | `/reception/admission-discharge-report` | `<app-admission-discharge-report>` | [`03_reception_admission_discharge_report`](./03_reception_admission_discharge_report/) | 8 عناصر | ✅ Discovery Completed |
| 04 | حجز العمليات | `/reception/surgery-booking` | `<app-surgery-booking>` | [`04_reception_surgery_booking`](./04_reception_surgery_booking/) | 12 عنصر | ✅ Discovery Completed |
| 05 | المرضى الداخلي قيد الخروج | `/waiting-list/leaving-requests` | `<app-leaving-requests>` | [`05_waiting_list_leaving_requests`](./05_waiting_list_leaving_requests/) | 10 عناصر | ✅ Discovery Completed |
| 06 | طلبات خروج المرضى | `/accountant/leaving-requests` | `<app-accom-leaving-wl>` | [`06_accountant_leaving_requests`](./06_accountant_leaving_requests/) | 7 عناصر | ✅ Discovery Completed |
| 07 | طلبات تحويل المرضى من الطوارئ | `/reception/emergency-transfers` | `<app-emergency-transfers>` | [`07_reception_emergency_transfers`](./07_reception_emergency_transfers/) | 4 عناصر | ✅ Discovery Completed |
| 08 | تقرير تأكيد طلبات المغادرة | `/reception/leaving-approval-report` | `<app-leaving-approval-report>` | [`08_reception_leaving_approval_report`](./08_reception_leaving_approval_report/) | 5 عناصر | ✅ Discovery Completed |

---

## 2. قائمة الاستعلامات (Info Desk) — (10 صفحات)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | عناصر `test-id` | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | بيانات الأطباء | `/info-desk/doctors` | `<app-doctors-list>` | [`info_desk_01_doctors`](./info_desk_01_doctors/) | 4 عناصر | ✅ Discovery Completed |
| 02 | بيانات مسؤولين الشيفت | `/info-desk/shift-managers` | `<app-shift-managers>` | [`info_desk_02_shift_managers`](./info_desk_02_shift_managers/) | 6 عناصر | ✅ Discovery Completed |
| 03 | قوائم الأسعار | `/info-desk/price-lists` | `<app-price-lists>` | [`info_desk_03_price_lists`](./info_desk_03_price_lists/) | 3 عناصر | ✅ Discovery Completed |
| 04 | أسماء العمليات | `/info-desk/surgery-names` | `<app-surgery-names>` | [`info_desk_04_surgery_names`](./info_desk_04_surgery_names/) | 3 عناصر | ✅ Discovery Completed |
| 05 | أسعار العمليات | `/info-desk/surgery-prices` | `<app-surgery-prices>` | [`info_desk_05_surgery_prices`](./info_desk_05_surgery_prices/) | 5 عناصر | ✅ Discovery Completed |
| 06 | أجندة العمليات | `/info-desk/surgery-agenda` | `<app-surgery-agenda>` | [`info_desk_06_surgery_agenda`](./info_desk_06_surgery_agenda/) | 7 عناصر | ✅ Discovery Completed |
| 07 | أجندة العيادات | `/info-desk/clinic-agenda` | `<app-clinic-agenda>` | [`info_desk_07_clinic_agenda`](./info_desk_07_clinic_agenda/) | 7 عناصر | ✅ Discovery Completed |
| 08 | دليل الهاتف | `/info-desk/phone-book` | `<app-phone-book-info-desk>` | [`info_desk_08_phone_book`](./info_desk_08_phone_book/) | 2 عنصر | ✅ Discovery Completed |
| 09 | قائمة انتظار العمليات | `/info-desk/surgeries` | `<app-surgeries-waiting>` | [`info_desk_09_surgeries`](./info_desk_09_surgeries/) | 4 عناصر | ✅ Discovery Completed |
| 10 | استعلام عن الباكيدجات | `/info-desk/packages` | `<app-packages>` | [`info_desk_10_packages`](./info_desk_10_packages/) | 15 عنصر | ✅ Discovery Completed |

---

## 3. قائمة المرضى المقيمين (Inpatients) — (6 صفحات)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | عناصر `test-id` | الحالة (Status) |
|---|---|---|---|---|---|---|
| 09 | المرضى بالغرف | `/reception/inpatients` | `<app-inpatient-list>` | [`09_inpatients_rooms`](./09_inpatients_rooms/) | 7 عناصر | ✅ Discovery Completed |
| 10 | المرضى بالرعاية المركزة | `/reception/icu` | `<app-inpatient-list>` | [`10_inpatients_icu`](./10_inpatients_icu/) | 7 عناصر | ✅ Discovery Completed |
| 11 | المرضى بالحضانة | `/reception/neonatal` | `<app-inpatient-list>` | [`11_inpatients_neonatal`](./11_inpatients_neonatal/) | 3 عناصر | ✅ Discovery Completed |
| 12 | مرافقو المرضى | `/reception/attendants` | `<app-attendant-list>` | [`12_inpatients_attendants`](./12_inpatients_attendants/) | 13 عنصر | ✅ Discovery Completed |
| 13 | إدارة الغرف | `/reception/room-management` | `<app-room-management>` | [`13_inpatients_room_management`](./13_inpatients_room_management/) | 7 عناصر | ✅ Discovery Completed |
| 14 | إشغال الغرف (خريطة) | `/reception/rooms` | `<app-accomodation-rooms>` | [`14_inpatients_rooms_map`](./14_inpatients_rooms_map/) | 2 عنصر | ✅ Discovery Completed |

---

## 4. قائمة الأشعة (Radiology) — (3 صفحات)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | عناصر `test-id` | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | قائمة انتظار الأشعة | `/rays/waiting-list` | `<app-rays-waiting-list>` | [`rays_01_waiting_list`](./rays_01_waiting_list/) | 13 عنصر | ✅ Discovery Completed |
| 02 | موقف تنفيذ حالات الأشعة وطباعة الاستيكر | `/rays/status` | `<app-rays-status>` | [`rays_02_status`](./rays_02_status/) | 10 عناصر | ✅ Discovery Completed |
| 03 | تقرير تفصيلي بالأشعة | `/rays/details` | `<app-rays-details>` | [`rays_03_details`](./rays_03_details/) | 12 عنصر | ✅ Discovery Completed |

---

## 5. قائمة المعمل وبنك الدم (Lab & Blood Bank) — (5 صفحات)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | عناصر `test-id` | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | قائمة انتظار التحاليل | `/lab/waiting-list` | `<app-lab-waiting-list>` | [`lab_01_waiting_list`](./lab_01_waiting_list/) | 14 عنصر | ✅ Discovery Completed |
| 02 | قائمة انتظار بنك الدم | `/lab/blood-waiting-list` | `<app-blood-waiting-list>` | [`lab_02_blood_waiting_list`](./lab_02_blood_waiting_list/) | 10 عناصر | ✅ Discovery Completed |
| 03 | تقرير بالتحاليل التفصيلي | `/lab/details` | `<app-lab-details>` | [`lab_03_details`](./lab_03_details/) | 15 عنصر | ✅ Discovery Completed |
| 04 | استعلام عن بنك الدم | `/lab/blood-bank-status` | `<app-blood-bank-status>` | [`lab_04_blood_bank_status`](./lab_04_blood_bank_status/) | 8 عناصر | ✅ Discovery Completed |
| 05 | استعلام عن نتائج التحاليل | `/lab/results-inquiry` | `<app-lab-results-inquiry>` | [`lab_05_results_inquiry`](./lab_05_results_inquiry/) | 14 عنصر | ✅ Discovery Completed |

---

## 6. قائمة العلاج الطبيعي (Physical Therapy) — (صفحة واحدة)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | عناصر `test-id` | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | قائمة انتظار العلاج الطبيعي | `/physical-therapy/waiting-list` | `<app-pt-waiting-list>` | [`physical_therapy_01_waiting_list`](./physical_therapy_01_waiting_list/) | 10 عناصر | ✅ Discovery Completed |

---

## 7. قائمة حسابات المرضى (Patient Accounts) — (6 صفحات)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | عناصر `test-id` | الحالة (Status) |
|---|---|---|---|---|---|---|
| 15 | كشوف الحساب المفتوحة | `/patient-accounts/unregistered-invoices` | `<app-unregistered-invoices>` | [`15_patient_unregistered_invoices`](./15_patient_unregistered_invoices/) | 37 عنصر | ✅ Discovery Completed |
| 16 | فواتير المرضى | `/patient-accounts/registered-invoices` | `<app-registered-invoices>` | [`16_patient_registered_invoices`](./16_patient_registered_invoices/) | 11 عنصر | ✅ Discovery Completed |
| 17 | حسابات المرضى الداخلي | `/patient-accounts/patient-checkups` | `<app-patient-checkups>` | [`17_patient_checkups`](./17_patient_checkups/) | 6 عناصر | ✅ Discovery Completed |
| 18 | مديونيات المرضى | `/patient-accounts/patient-settlements` | `<app-patient-settlements>` | [`18_patient_settlements`](./18_patient_settlements/) | 8 عناصر | ✅ Discovery Completed |
| 19 | بنك الفنيين | `/patient-accounts/technician-bank` | `<app-technician-bank>` | [`19_patient_technician_bank`](./19_patient_technician_bank/) | 15 عنصر | ✅ Discovery Completed |
| 20 | دمج بين المرضى | `/patient-accounts/merge-patients` | `<app-merge-patients>` | [`20_patient_merge`](./20_patient_merge/) | 4 عناصر | ✅ Discovery Completed |

---

## 8. قائمة سكرتارية التمريض (Nursing Secretary) — (6 صفحات)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | عناصر `test-id` | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | المرضى بالغرف (تمريض) | `/waiting-list/accomodation-rooms` | `<app-nursing-secretary>` | [`nursing_01_rooms`](./nursing_01_rooms/) | 7 عناصر | ✅ Discovery Completed |
| 02 | المرضى بالرعاية المركزة (تمريض) | `/waiting-list/icu` | `<app-nursing-secretary>` | [`nursing_02_icu`](./nursing_02_icu/) | 7 عناصر | ✅ Discovery Completed |
| 03 | المرضى بالحضانة (تمريض) | `/waiting-list/neonatal` | `<app-nursing-secretary>` | [`nursing_03_neonatal`](./nursing_03_neonatal/) | 3 عناصر | ✅ Discovery Completed |
| 04 | طلبات الأنظمة الغذائية للمرضى | `/waiting-list/patient-diets-list` | `<app-patient-diets-list>` | [`nursing_04_patient_diets`](./nursing_04_patient_diets/) | 5 عناصر | ✅ Discovery Completed |
| 05 | طلبات الأنظمة الغذائية للمرافقين | `/waiting-list/attendant-diets` | `<app-attendant-diets>` | [`nursing_05_attendant_diets`](./nursing_05_attendant_diets/) | 4 عناصر | ✅ Discovery Completed |
| 06 | التقارير الطبية للمرضى الداخلي | `/waiting-list/medical-reports` | `<app-medical-reports>` | [`nursing_06_medical_reports`](./nursing_06_medical_reports/) | 11 عنصر | ✅ Discovery Completed |

---

## 9. قائمة العيادات الخارجية (Outpatient Clinics) — (6 صفحات)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | عناصر `test-id` | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | قائمة انتظار العيادات | `/clinic/waiting-list` | `<app-clinic-waiting-list>` | [`clinic_01_waiting_list`](./clinic_01_waiting_list/) | 6 عناصر | ✅ Discovery Completed |
| 02 | تقرير العيادات التفصيلي | `/clinic/visit-details-report` | `<app-visit-details-report>` | [`clinic_02_visit_details_report`](./clinic_02_visit_details_report/) | 13 عنصر | ✅ Discovery Completed |
| 03 | المرضى بالعيادات | `/clinic/patients` | `<app-patients-in-clinics>` | [`clinic_03_patients`](./clinic_03_patients/) | 13 عنصر | ✅ Discovery Completed |
| 04 | تعديل زيارة عيادات | `/clinic/edit-visit` | `<app-edit-visit>` | [`clinic_04_edit_visit`](./clinic_04_edit_visit/) | 13 عنصر | ✅ Discovery Completed |
| 05 | إلغاء خروج مريض عيادات مُغلقة | `/clinic/cancel-leaved-visit` | `<app-cancel-leaved-visit>` | [`clinic_05_cancel_leaved_visit`](./clinic_05_cancel_leaved_visit/) | 4 عناصر | ✅ Discovery Completed |
| 06 | التقارير الطبية للعيادات الخارجية | `/clinic/medical-reports` | `<app-visit-medical-reports>` | [`clinic_06_medical_reports`](./clinic_06_medical_reports/) | 12 عنصر | ✅ Discovery Completed |

---

## 10. قائمة الإسعاف والطوارئ (Emergency) — (6 صفحات)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | عناصر `test-id` | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | المرضى بالطوارئ | `/emergency/waiting-list` | `<app-emergency-waiting-list>` | [`emergency_01_waiting_list`](./emergency_01_waiting_list/) | 8 عناصر | ✅ Discovery Completed |
| 02 | تعديل زيارة بالطوارئ | `/emergency/edit-visit` | `<app-edit-emergency-visit>` | [`emergency_02_edit_visit`](./emergency_02_edit_visit/) | 4 عناصر | ✅ Discovery Completed |
| 03 | تقرير الدخول والخروج بالطوارئ | `/emergency/admission-discharge-report` | `<app-emergency-cases-report>` | [`emergency_03_admission_discharge_report`](./emergency_03_admission_discharge_report/) | 5 عناصر | ✅ Discovery Completed |
| 04 | التقارير الطبية للإسعاف والطوارئ | `/emergency/medical-reports` | `<app-emergency-medical-reports>` | [`emergency_04_medical_reports`](./emergency_04_medical_reports/) | 1 عنصر | ✅ Discovery Completed |
| 05 | تقرير إشغال أسرة الطوارئ | `/emergency/bed-occupancy` | `<app-emergency-bed-occupancy>` | [`emergency_05_bed_occupancy`](./emergency_05_bed_occupancy/) | 1 عنصر | ✅ Discovery Completed |
| 06 | إلغاء خروج مريض طوارئ تم إغلاقها | `/emergency/cancel-leaved` | `<app-cancel-leaved-emergency>` | [`emergency_06_cancel_leaved`](./emergency_06_cancel_leaved/) | 4 عناصر | ✅ Discovery Completed |

---

## 11. قائمة تقارير المبيعات (Sales Reports) — (9 صفحات)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | محددات العناصر | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | كل تقارير المبيعات | `/reports/sales` | `<app-sales-reports>` | [`sales_01_all_sales`](./sales_01_all_sales/) | 7 محددات | ✅ Discovery Completed |
| 02 | مبيعات العيادات | `/reports/clinic-sales-in-period` | `<app-extended-report-page>` | [`sales_02_clinic_sales`](./sales_02_clinic_sales/) | 7 محددات | ✅ Discovery Completed |
| 03 | مبيعات الطوارئ التفصيلي | `/reports/emergency-services-sales` | `<app-extended-report-page>` | [`sales_03_emergency_detailed`](./sales_03_emergency_detailed/) | 7 محددات | ✅ Discovery Completed |
| 04 | مبيعات طوارئ المستشفى | `/reports/hospital-emergency-sales` | `<app-extended-report-page>` | [`sales_04_hospital_emergency`](./sales_04_hospital_emergency/) | 7 محددات | ✅ Discovery Completed |
| 05 | مبيعات العيادات اجمالى | `/reports/opd-sales-report` | `<app-extended-report-page>` | [`sales_05_opd_totals`](./sales_05_opd_totals/) | 7 محددات | ✅ Discovery Completed |
| 06 | مبيعات الداخلى تفصيلى | `/reports/accommodation-class-checkup` | `<app-extended-report-page>` | [`sales_06_inpatient_detailed`](./sales_06_inpatient_detailed/) | 7 محددات | ✅ Discovery Completed |
| 07 | مبيعات الداخلى اجمالى | `/reports/acc-class-checkup-totals` | `<app-extended-report-page>` | [`sales_07_inpatient_totals`](./sales_07_inpatient_totals/) | 7 محددات | ✅ Discovery Completed |
| 08 | ربحية حالات الداخلي | `/reports/ipd-case-profitability` | `<app-extended-report-page>` | [`sales_08_ipd_profitability`](./sales_08_ipd_profitability/) | 7 محددات | ✅ Discovery Completed |
| 09 | مبيعات الداخلي باكدج | `/reports/checkup-with-package` | `<app-extended-report-page>` | [`sales_09_package_sales`](./sales_09_package_sales/) | 7 محددات | ✅ Discovery Completed |

---

## 12. قائمة تقارير تحليلية (Analytical Reports) — (23 صفحة)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | محددات العناصر | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | كل التقارير التحليلية | `/reports/analytical` | `<app-analytical-reports>` | [`analytical_01_all_reports`](./analytical_01_all_reports/) | 2 محدد | ✅ Discovery Completed |
| 02 | تقرير عمليات المرضى | `/reports/surgery-with-tax-total` | `<app-extended-report-page>` | [`analytical_02_surgery_with_tax`](./analytical_02_surgery_with_tax/) | 7 محددات | ✅ Discovery Completed |
| 03 | خدمات المستشفى والأجهزة | `/reports/hospital-services-devices` | `<app-extended-report-page>` | [`analytical_03_hospital_services_devices`](./analytical_03_hospital_services_devices/) | 7 محددات | ✅ Discovery Completed |
| 04 | إيرادات قسم المرضى الداخلي/العناية المركزة | `/reports/ipd-icu-revenue` | `<app-extended-report-page>` | [`analytical_04_ipd_icu_revenue`](./analytical_04_ipd_icu_revenue/) | 7 محددات | ✅ Discovery Completed |
| 05 | إجمالي إيرادات المستشفى - مفصل | `/reports/detailed-hospital-revenue` | `<app-extended-report-page>` | [`analytical_05_detailed_hospital_revenue`](./analytical_05_detailed_hospital_revenue/) | 7 محددات | ✅ Discovery Completed |
| 06 | إجمالي إيرادات المستشفى | `/reports/hospital-revenue-comparison` | `<app-extended-report-page>` | [`analytical_06_hospital_revenue_comparison`](./analytical_06_hospital_revenue_comparison/) | 7 محددات | ✅ Discovery Completed |
| 07 | خدمات العمليات بالنوع | `/reports/surgery-services-by-type` | `<app-extended-report-page>` | [`analytical_07_surgery_services_by_type`](./analytical_07_surgery_services_by_type/) | 7 محددات | ✅ Discovery Completed |
| 08 | خدمات الاقامة بالنوع | `/reports/accommodation-services-by-type` | `<app-extended-report-page>` | [`analytical_08_accommodation_services_by_type`](./analytical_08_accommodation_services_by_type/) | 7 محددات | ✅ Discovery Completed |
| 09 | اجمالي الايرادات بالتخصص و الطبيب | `/reports/doctors-departments-revenue` | `<app-extended-report-page>` | [`analytical_09_doctors_departments_revenue`](./analytical_09_doctors_departments_revenue/) | 7 محددات | ✅ Discovery Completed |
| 10 | مرتبات الأطباء عن عمليات (داخلي) | `/reports/doctor-inpatient-surgery-salaries` | `<app-extended-report-page>` | [`analytical_10_doctor_inpatient_surgery_salaries`](./analytical_10_doctor_inpatient_surgery_salaries/) | 7 محددات | ✅ Discovery Completed |
| 11 | مرتبات اطباء العيادات | `/reports/opd-doctors-specialty-revenue` | `<app-extended-report-page>` | [`analytical_11_opd_doctors_specialty_revenue`](./analytical_11_opd_doctors_specialty_revenue/) | 7 محددات | ✅ Discovery Completed |
| 12 | أتعاب الأطباء (عيادات + عمليات) | `/reports/doctors-clinics-surgeries-fees` | `<app-extended-report-page>` | [`analytical_12_doctors_clinics_surgeries_fees`](./analytical_12_doctors_clinics_surgeries_fees/) | 7 محددات | ✅ Discovery Completed |
| 13 | إجمالي الإيراد بالحالة (الفواتير المسجلة) | `/reports/revenue-billed-by-case` | `<app-extended-report-page>` | [`analytical_13_revenue_billed_by_case`](./analytical_13_revenue_billed_by_case/) | 7 محددات | ✅ Discovery Completed |
| 14 | إجمالي الإيراد بالحالة (الفواتير الغير مسجلة) | `/reports/revenue-unbilled-by-case` | `<app-extended-report-page>` | [`analytical_14_revenue_unbilled_by_case`](./analytical_14_revenue_unbilled_by_case/) | 7 محددات | ✅ Discovery Completed |
| 15 | إجمالي الإيرادات بالقطاع | `/reports/total-revenue-by-department` | `<app-extended-report-page>` | [`analytical_15_total_revenue_by_department`](./analytical_15_total_revenue_by_department/) | 7 محددات | ✅ Discovery Completed |
| 16 | إيرادات المعمل بالقطاع | `/reports/lab-revenue-by-department` | `<app-extended-report-page>` | [`analytical_16_lab_revenue_by_department`](./analytical_16_lab_revenue_by_department/) | 7 محددات | ✅ Discovery Completed |
| 17 | إيرادات الأشعة بالقطاع | `/reports/radiology-revenue-by-department` | `<app-extended-report-page>` | [`analytical_17_radiology_revenue_by_department`](./analytical_17_radiology_revenue_by_department/) | 7 محددات | ✅ Discovery Completed |
| 18 | إيرادات بنك الدم بالقطاع | `/reports/blood-bank-revenue-by-department` | `<app-extended-report-page>` | [`analytical_18_blood_bank_revenue_by_department`](./analytical_18_blood_bank_revenue_by_department/) | 7 محددات | ✅ Discovery Completed |
| 19 | إيرادات الصيدلية بالقطاع | `/reports/pharmacy-revenue-by-department` | `<app-extended-report-page>` | [`analytical_19_pharmacy_revenue_by_department`](./analytical_19_pharmacy_revenue_by_department/) | 7 محددات | ✅ Discovery Completed |
| 20 | إيرادات العمليات بنوع الحالة | `/reports/surgery-revenue-by-case-type` | `<app-extended-report-page>` | [`analytical_20_surgery_revenue_by_case_type`](./analytical_20_surgery_revenue_by_case_type/) | 7 محددات | ✅ Discovery Completed |
| 21 | إيرادات الرعاية المركزة | `/reports/icu-revenue-summary` | `<app-extended-report-page>` | [`analytical_21_icu_revenue_summary`](./analytical_21_icu_revenue_summary/) | 7 محددات | ✅ Discovery Completed |
| 22 | إيرادات العيادات الخارجية | `/reports/opd-revenue-summary` | `<app-extended-report-page>` | [`analytical_22_opd_revenue_summary`](./analytical_22_opd_revenue_summary/) | 7 محددات | ✅ Discovery Completed |
| 23 | بيان إحصائي مترددين وإيرادات | `/reports/statistical-report` | `<app-extended-report-page>` | [`analytical_23_statistical_report`](./analytical_23_statistical_report/) | 7 محددات | ✅ Discovery Completed |

---

## 13. قائمة التقارير العامة (General Reports) — (44 صفحة)
| # | الصفحة (DDL) | المسار (Route) | المكون (Angular Component) | الفولدر | محددات العناصر | الحالة (Status) |
|---|---|---|---|---|---|---|
| 01 | أتعاب طبيب | `/reports/doctor-fees` | `<app-extended-report-page>` | [`reports_01_doctor_fees`](./reports_01_doctor_fees/) | 7 محددات | ✅ Discovery Completed |
| 02 | أتعاب مرور الاستشاريين | `/reports/doctor-fees-supervisors` | `<app-extended-report-page>` | [`reports_02_doctor_fees_supervisors`](./reports_02_doctor_fees_supervisors/) | 7 محددات | ✅ Discovery Completed |
| 03 | عمليات طبيب | `/reports/doctor-surgeries` | `<app-extended-report-page>` | [`reports_03_doctor_surgeries`](./reports_03_doctor_surgeries/) | 7 محددات | ✅ Discovery Completed |
| 04 | مطالبات خدمات جهة | `/reports/client-obtained-services` | `<app-extended-report-page>` | [`reports_04_client_obtained_services`](./reports_04_client_obtained_services/) | 7 محددات | ✅ Discovery Completed |
| 05 | الخدمات حسب التخصص | `/reports/specialist-obtained-services` | `<app-extended-report-page>` | [`reports_05_specialist_obtained_services`](./reports_05_specialist_obtained_services/) | 7 محددات | ✅ Discovery Completed |
| 06 | حركات الخزينة | `/reports/income-in-duration` | `<app-extended-report-page>` | [`reports_06_income_in_duration`](./reports_06_income_in_duration/) | 7 محددات | ✅ Discovery Completed |
| 07 | المصروفات خلال فترة | `/reports/expenses-in-duration` | `<app-extended-report-page>` | [`reports_07_expenses_in_duration`](./reports_07_expenses_in_duration/) | 7 محددات | ✅ Discovery Completed |
| 08 | الإقامة خلال فترة | `/reports/accommodation-in-duration` | `<app-extended-report-page>` | [`reports_08_accommodation_in_duration`](./reports_08_accommodation_in_duration/) | 7 محددات | ✅ Discovery Completed |
| 09 | تسويات الأطباء | `/reports/doctors-settlements` | `<app-extended-report-page>` | [`reports_09_doctors_settlements`](./reports_09_doctors_settlements/) | 7 محددات | ✅ Discovery Completed |
| 10 | إقامات المريض داخل المستشفى | `/reports/patient-transferring-accommodation` | `<app-extended-report-page>` | [`reports_10_patient_transferring_accommodation`](./reports_10_patient_transferring_accommodation/) | 7 محددات | ✅ Discovery Completed |
| 11 | تقرير بالعمليات خلال فترة | `/reports/surgeries-in-period` | `<app-extended-report-page>` | [`reports_11_surgeries_in_period`](./reports_11_surgeries_in_period/) | 7 محددات | ✅ Discovery Completed |
| 12 | خدمات المرضى خلال فترة | `/reports/services-patients` | `<app-extended-report-page>` | [`reports_12_services_patients`](./reports_12_services_patients/) | 7 محددات | ✅ Discovery Completed |
| 13 | تحليل الايرادات الطوارئ خلال فترة | `/reports/balance-clinic-external-period` | `<app-extended-report-page>` | [`reports_13_balance_clinic_external_period`](./reports_13_balance_clinic_external_period/) | 7 محددات | ✅ Discovery Completed |
| 14 | تحليل الايرادات الخارجي خلال فترة | `/reports/balance-clinic-external-patients` | `<app-extended-report-page>` | [`reports_14_balance_clinic_external_patients`](./reports_14_balance_clinic_external_patients/) | 7 محددات | ✅ Discovery Completed |
| 15 | اجمالى على مستوى العياده | `/reports/total-invoice-by-clinic` | `<app-extended-report-page>` | [`reports_15_total_invoice_by_clinic`](./reports_15_total_invoice_by_clinic/) | 7 محددات | ✅ Discovery Completed |
| 16 | اجمالى على مستوى الطبيب | `/reports/total-invoice-by-doctor` | `<app-extended-report-page>` | [`reports_16_total_invoice_by_doctor`](./reports_16_total_invoice_by_doctor/) | 7 محددات | ✅ Discovery Completed |
| 17 | الخدمات المحذوفة لمريض | `/reports/deleted-patient-services` | `<app-extended-report-page>` | [`reports_17_deleted_patient_services`](./reports_17_deleted_patient_services/) | 7 محددات | ✅ Discovery Completed |
| 18 | الايرادات والمصروفات اليوميه | `/reports/daily-balance-clinic` | `<app-extended-report-page>` | [`reports_18_daily_balance_clinic`](./reports_18_daily_balance_clinic/) | 7 محددات | ✅ Discovery Completed |
| 19 | مرور الاشراف الطبى | `/reports/supervisor-medical-pass` | `<app-extended-report-page>` | [`reports_19_supervisor_medical_pass`](./reports_19_supervisor_medical_pass/) | 7 محددات | ✅ Discovery Completed |
| 20 | تقرير بخروج المرضى | `/reports/patients-leave-reasons` | `<app-extended-report-page>` | [`reports_20_patients_leave_reasons`](./reports_20_patients_leave_reasons/) | 7 محددات | ✅ Discovery Completed |
| 21 | تقرير تفصيلي بالخدمات والمستلزمات الطبية | `/reports/services-medical-supplies` | `<app-extended-report-page>` | [`reports_21_services_medical_supplies`](./reports_21_services_medical_supplies/) | 7 محددات | ✅ Discovery Completed |
| 22 | تقرير باستهلاك الاجهزة | `/reports/used-devices` | `<app-extended-report-page>` | [`reports_22_used_devices`](./reports_22_used_devices/) | 7 محددات | ✅ Discovery Completed |
| 23 | تقرير باستهلاك الغازات | `/reports/used-surgery-gases` | `<app-extended-report-page>` | [`reports_23_used_surgery_gases`](./reports_23_used_surgery_gases/) | 7 محددات | ✅ Discovery Completed |
| 24 | الخدمات بنوع الخروج | `/reports/services-by-leave-type` | `<app-extended-report-page>` | [`reports_24_services_by_leave_type`](./reports_24_services_by_leave_type/) | 7 محددات | ✅ Discovery Completed |
| 25 | الدخول خلال فترة | `/reports/entrance-patients` | `<app-extended-report-page>` | [`reports_25_entrance_patients`](./reports_25_entrance_patients/) | 7 محددات | ✅ Discovery Completed |
| 26 | فواتير الداخلى خلال فتره | `/reports/internal-invoices` | `<app-extended-report-page>` | [`reports_26_internal_invoices`](./reports_26_internal_invoices/) | 7 محددات | ✅ Discovery Completed |
| 27 | فواتير الطوارئ خلال فتره | `/reports/emergency-invoices` | `<app-extended-report-page>` | [`reports_27_emergency_invoices`](./reports_27_emergency_invoices/) | 7 محددات | ✅ Discovery Completed |
| 28 | بنود الفواتير الداخلى | `/reports/internal-invoice-line-codes` | `<app-extended-report-page>` | [`reports_28_internal_invoice_line_codes`](./reports_28_internal_invoice_line_codes/) | 7 محددات | ✅ Discovery Completed |
| 29 | تقرير العمليات المؤجلة / الملغاه | `/reports/cancelled-delayed-surgeries` | `<app-extended-report-page>` | [`reports_29_cancelled_delayed_surgeries`](./reports_29_cancelled_delayed_surgeries/) | 7 محددات | ✅ Discovery Completed |
| 30 | تقرير بمدفوعات المرضى | `/reports/patient-payment-orders` | `<app-extended-report-page>` | [`reports_30_patient_payment_orders`](./reports_30_patient_payment_orders/) | 7 محددات | ✅ Discovery Completed |
| 31 | تقرير بتعديلات بيانات المرضى | `/reports/patient-data-changes` | `<app-extended-report-page>` | [`reports_31_patient_data_changes`](./reports_31_patient_data_changes/) | 7 محددات | ✅ Discovery Completed |
| 32 | تقرير بخصومات الفواتير | `/reports/inpatient-invoice-discounts` | `<app-extended-report-page>` | [`reports_32_inpatient_invoice_discounts`](./reports_32_inpatient_invoice_discounts/) | 7 محددات | ✅ Discovery Completed |
| 33 | تغييرات درجات العمليات | `/reports/surgery-degree-changes` | `<app-extended-report-page>` | [`reports_33_surgery_degree_changes`](./reports_33_surgery_degree_changes/) | 7 محددات | ✅ Discovery Completed |
| 34 | النظام الغذائى لمريض | `/reports/patient-diet-list` | `<app-extended-report-page>` | [`reports_34_patient_diet_list`](./reports_34_patient_diet_list/) | 7 محددات | ✅ Discovery Completed |
| 35 | تغييرات الاقامة خلال فترة | `/reports/accommodation-degree-changes` | `<app-extended-report-page>` | [`reports_35_accommodation_degree_changes`](./reports_35_accommodation_degree_changes/) | 7 محددات | ✅ Discovery Completed |
| 36 | تقرير بخصومات العيادات | `/reports/clinic-discounts` | `<app-extended-report-page>` | [`reports_36_clinic_discounts`](./reports_36_clinic_discounts/) | 7 محددات | ✅ Discovery Completed |
| 37 | تقرير بيانات المرضى | `/reports/patient-data-search` | `<app-extended-report-page>` | [`reports_37_patient_data_search`](./reports_37_patient_data_search/) | 7 محددات | ✅ Discovery Completed |
| 38 | تقرير تشخيصات المرضى | `/reports/clinic-diagnoses-search` | `<app-extended-report-page>` | [`reports_38_clinic_diagnoses_search`](./reports_38_clinic_diagnoses_search/) | 7 محددات | ✅ Discovery Completed |
| 39 | تقرير المرافقين | `/reports/attendants-report` | `<app-extended-report-page>` | [`reports_39_attendants_report`](./reports_39_attendants_report/) | 7 محددات | ✅ Discovery Completed |
| 40 | صافى الادويه لمريض | `/reports/reservation-waiting-list` | `<app-extended-report-page>` | [`reports_40_reservation_waiting_list`](./reports_40_reservation_waiting_list/) | 7 محددات | ✅ Discovery Completed |
| 41 | تقرير وجبات المرضي | `/reports/patient-meals-report` | `<app-extended-report-page>` | [`reports_41_patient_meals_report`](./reports_41_patient_meals_report/) | 7 محددات | ✅ Discovery Completed |
| 42 | تقرير زيارات المستشفي خلال فترة | `/reports/hospital-sob-visits` | `<app-extended-report-page>` | [`reports_42_hospital_sob_visits`](./reports_42_hospital_sob_visits/) | 7 محددات | ✅ Discovery Completed |
| 43 | تقرير بعدد حالات العيادات | `/reports/clinics-case-count` | `<app-extended-report-page>` | [`reports_43_clinics_case_count`](./reports_43_clinics_case_count/) | 7 محددات | ✅ Discovery Completed |
| 44 | تفاصيل الخصومات خلال فترة | `/reports/clinic-discount-analysis` | `<app-extended-report-page>` | [`reports_44_clinic_discount_analysis`](./reports_44_clinic_discount_analysis/) | 7 محددات | ✅ Discovery Completed |

---

## 14. ملخص اكتمال مرحلة الاستكشاف (Discovery Phase Status)
🎉 **تم اكتمال استكشاف وتوثيق كافة القوائم الـ 13 في شريط التنقل (Navbar) بنسبة 100%!**
- **إجمالي الصفحات الموثقة:** 134 صفحة ومكون.
- **قاعدة المعرفة المركزية:** تم توثيق وحفظ كافة المحددات، وهياكل الـ DOM، وسيناريوهات الفحص في [`KNOWLEDGE_BASE.json`](./KNOWLEDGE_BASE.json).
- **الملاحظات والعيوب:** تم تدوين الملاحظات المعمارية ومشاكل الـ test-id المفقودة في [`observations.md`](./observations.md).
