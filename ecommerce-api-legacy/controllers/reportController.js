const { dbAll } = require('../database');

const getFinancialReport = async (req, res, next) => {
    try {
        // Optimized LEFT JOIN Query to solve the N+1 problem completely
        const query = `
            SELECT 
                c.id AS course_id, 
                c.title AS course_title, 
                u.name AS student_name, 
                p.amount AS payment_amount, 
                p.status AS payment_status
            FROM courses c
            LEFT JOIN enrollments e ON e.course_id = c.id
            LEFT JOIN users u ON e.user_id = u.id
            LEFT JOIN payments p ON p.enrollment_id = e.id
        `;

        const rows = await dbAll(query);

        // Group rows by course_id to construct the exact original structure
        const reportMap = {};

        rows.forEach(row => {
            const courseId = row.course_id;

            if (!reportMap[courseId]) {
                reportMap[courseId] = {
                    course: row.course_title,
                    revenue: 0,
                    students: []
                };
            }

            // If there's an enrollment, process user and payment details
            if (row.student_name !== null) {
                const paidAmount = row.payment_amount || 0;
                
                if (row.payment_status === 'PAID') {
                    reportMap[courseId].revenue += paidAmount;
                }

                reportMap[courseId].students.push({
                    student: row.student_name || 'Unknown',
                    paid: paidAmount
                });
            }
        });

        // Convert the map back to an array to match the expected format
        const report = Object.values(reportMap);

        return res.status(200).json(report);
    } catch (err) {
        next(err);
    }
};

module.exports = { getFinancialReport };
