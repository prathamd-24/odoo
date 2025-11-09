# OneFlow: Plan to Bill in One Place

> **A unified, modular Project Management System where teams can Plan, Execute, and Bill — all within one elegant glassmorphism dashboard.**

## Team Details: Team 63
- Pratham Desai
- Harry Mehta
- Kevin Desai
- Pratham Mehta
- Demo Video link: [video](https://drive.google.com/file/d/1VeH149MZNrIN12ew_KizCdaeaYHsWYuu/view?usp=sharing)

---

## 🎯 Core Vision

OneFlow is a comprehensive project management platform designed for agencies and small teams to manage the complete project lifecycle from planning through execution to billing. The system provides role-based access, real-time collaboration, financial tracking, and actionable analytics in a modern glassmorphism interface.

---

## 👥 User Roles & Permissions

### Project Manager (PM)
- Create, edit, and delete projects
- Assign team members to projects and tasks
- Manage and track task progress
- Approve timesheets and expenses
- Trigger invoice generation
- Monitor project budgets and profitability

### Team Member
- View assigned projects and tasks
- Update task status and progress
- Log working hours via timesheets
- Submit expenses with receipts
- Add comments and file attachments
- Collaborate on task completion

### Sales/Finance
- Create and manage Sales Orders (SO)
- Create and manage Purchase Orders (PO)
- Generate customer invoices
- Process vendor bills
- Track financial records per project
- Manage revenue and cost tracking

### Admin
- Full system access (superuser)
- Manage all users, roles, and permissions
- Configure products, partners, and master data
- Access all modules and analytics
- System-wide settings and configurations

---

## 🏗️ System Architecture

### Technology Stack
- **Frontend**: React + TypeScript + Vite
- **UI Library**: Shadcn/ui components with glassmorphism theme
- **Styling**: Tailwind CSS with custom glass tokens
- **Backend**: Python Flask
- **Database**: MySQL with normalized schema (3NF/BCNF)
- **State Management**: React hooks and context
- **Routing**: React Router

---

## 📦 Core Functional Modules

### A. User Authentication & Identity

#### Features:
- **Secure Login/Signup** with role detection
- **Role-based Dashboard** routing upon authentication
- **Password Management** (reset, change, recovery)
- **Profile Management** (update personal info, avatar, contact details)
- **Multi-role Support** (users can have multiple roles)
- **Session Management** with secure token handling

---

### B. Dashboard & Navigation

#### Central Dashboard:
- **Project Overview Cards** displaying all active projects
- **Status Filtering**: Planned / In Progress / Completed / On Hold / Cancelled
- **KPI Widgets**:
  - Active Projects count
  - Delayed Tasks alert
  - Hours Logged (current week)
  - Revenue Earned (YTD)
- **Recent Activity Feed** (task updates, comments, financial events)
- **Quick Actions** floating button for rapid creation

#### Navigation System:
- **Collapsible Glass Sidebar** (260px)
  - Logo and app branding
  - User avatar with role selector
  - Primary navigation links
  - Quick-create floating button
- **Global Topbar**:
  - Unified search (projects, tasks, documents, partners)
  - Quick filters
  - Notifications bell
  - User menu (profile, settings, logout)
  - Contextual breadcrumbs

---

### C. Project Management

#### Project Features:
- **Full CRUD Operations** (Create, Read, Update, Delete)
- **Project Attributes**:
  - Unique project code
  - Name and description
  - Assigned Project Manager
  - Team member assignments
  - Start and end dates
  - Budget allocation
  - Status tracking
- **Visual Progress Tracking**:
  - Progress percentage bar
  - Budget utilization gauge
  - Task completion metrics
- **Quick Links Panel**:
  - Associated Sales Orders
  - Purchase Orders
  - Customer Invoices
  - Vendor Bills
  - Expense submissions

#### Project Views:
- **List View**: Sortable table with all project attributes
- **Card View**: Visual cards with key metrics
- **Filtering**: By status, PM, date range
- **Grouping**: By status or Project Manager
- **Search**: By project code or name

---

### D. Task Management

#### Task Operations:
- **Task CRUD** within projects
- **Task Attributes**:
  - Title and description
  - Assigned users (multi-select)
  - Due dates
  - Priority levels (Low, Medium, High, Urgent)
  - Status states (New, In Progress, Blocked, Done)
- **Collaboration Features**:
  - Comments and threaded discussions
  - File attachments (drag & drop)
  - Activity timeline
  - @mentions for team members

#### Task Views:
- **List View**: Comprehensive table with filters
- **Kanban Board**: Drag-and-drop cards across columns
- **My Tasks / All Tasks** toggle
- **Inline Editing** for quick status updates

#### Task Detail Modal:
- Full task information
- Activity timeline with comments
- Attached files with preview
- Linked timesheets
- Related invoice lines
- Quick actions (Log Time, Add Expense)

---

### E. Financial Operations

#### 1. Sales Orders (SO)
- **Purpose**: Document what the customer purchases
- **Features**:
  - SO number generation
  - Link to project and customer
  - Order date tracking
  - Status management (Draft, Confirmed, Cancelled, Closed)
  - Multi-currency support
  - Line items with products
  - Quantity, unit price, line totals
  - Milestone flagging
  - Notes and attachments
- **Workflow**: Create SO → Link to project → Generate invoice from lines

#### 2. Purchase Orders (PO)
- **Purpose**: Track company spending with vendors
- **Features**:
  - PO number generation
  - Link to project and vendor
  - Order date tracking
  - Status management
  - Line items with products/services
  - Quantity, unit cost, line totals
  - Link to vendor bills
- **Workflow**: Create PO → Receive goods/services → Create vendor bill

#### 3. Customer Invoices
- **Purpose**: Bill customers for work completed
- **Features**:
  - Invoice number generation
  - Link to project and customer
  - Invoice and due dates
  - Status tracking (Draft, Posted, Paid, Void)
  - Multi-currency support
  - Line items with flexible sources:
    - From Sales Order lines
    - From approved timesheets
    - From billable expenses
    - Manual entry
  - Automatic total calculations
  - Notes and terms
- **Workflow**: Create from SO/timesheets → Review → Post → Mark paid

#### 4. Vendor Bills
- **Purpose**: Track amounts payable to suppliers
- **Features**:
  - Bill number tracking
  - Link to project and vendor
  - Bill and due dates
  - Status management
  - Line items linked to PO lines
  - Cost tracking for profitability
- **Workflow**: Receive bill → Link to PO → Approve → Mark paid

#### 5. Expenses
- **Purpose**: Track team expenses (travel, materials, etc.)
- **Features**:
  - Submission by team members
  - Link to project and task
  - Expense date and description
  - Amount tracking
  - Billable/Non-billable toggle
  - Receipt upload
  - Approval workflow
  - Status tracking (Submitted, Approved, Rejected, Reimbursed)
  - Optional linking to customer invoice
- **Workflow**: Submit → PM approves → Reimburse/Bill to customer

#### Global Financial Lists:
- Comprehensive lists for all financial documents
- Search and filter capabilities
- Group by project, partner, status, date range
- Export functionality
- Bulk operations

---

### F. Timesheet Management

#### Timesheet Features:
- **Time Logging**:
  - Per person, task, date
  - Hours worked (decimal precision)
  - Billable/Non-billable toggle
  - Session notes
- **Rate Management**:
  - Employee hourly rates (admin-configured)
  - Internal cost rate tracking
  - Automatic cost amount calculation
- **Status Workflow**: Logged → Approved → Billed
- **Billing Integration**:
  - Link timesheets to invoice lines
  - Aggregate timesheets for batch billing
  - Track billed vs unbilled hours

#### Timesheet Views:
- **Calendar View**: Visual time tracking by date
- **Table View**: Detailed list with all attributes
- **Weekly Summary**: Hours by project and task
- **Bulk Actions**: Approve multiple timesheets, generate invoices

---

### G. Analytics & Reporting

#### Dashboard KPIs:
- **Project Metrics**:
  - Total Projects count
  - Projects by status
  - On-time delivery rate
- **Task Metrics**:
  - Tasks Completed
  - Delayed Tasks
  - Task completion velocity
- **Time Metrics**:
  - Total Hours Logged
  - Billable vs Non-billable hours
  - Resource utilization rate
- **Financial Metrics**:
  - Revenue booked
  - Costs incurred
  - Gross profit
  - Profit margins

#### Visual Analytics:
- **Project Progress Charts**: Stacked bar per milestone
- **Resource Utilization**: Stacked area chart by user/week
- **Cost vs Revenue**: Dual-axis line/area chart
- **Profitability Heatmap**: Calendar view of project delays
- **Burn-down Charts**: Time tracked vs planned hours
- **Budget Tracking**: Actual vs planned budget per project

#### Project-Level Analytics:
- **Profitability Dashboard**:
  - Revenue breakdown (invoices)
  - Cost breakdown (bills, timesheets, expenses)
  - Net profit calculation
  - Margin percentage
- **Trend Analysis**: Historical performance over time
- **Comparative Views**: Project-to-project comparisons

---

### H. Contextual Workflow Panels

#### Project Links Panel:
- **Quick Access** to all project-related documents
- **Filtered Views**:
  - Sales Orders linked to project
  - Purchase Orders for project costs
  - Customer Invoices for revenue
  - Vendor Bills for expenses
  - Team expense submissions
- **One-Click Actions**:
  - Create invoice from SO
  - Convert timesheet to invoice line
  - Link PO to vendor bill
  - Approve expenses

---

### I. Settings & Configuration

#### Master Data Management:
- **Partners** (Customers & Vendors):
  - Company name and type
  - Contact information
  - Tax ID and billing addresses
  - Payment terms
- **Products & Services**:
  - SKU and name
  - Description
  - Unit of measure
  - Default pricing
- **Users & Teams**:
  - User accounts
  - Role assignments
  - Hourly rates
  - Active status

#### System Settings:
- **Company Information**
- **Currency Preferences**
- **Invoice/Document Numbering**
- **Email Templates**
- **Notification Preferences**
- **Accessibility Options** (motion reduction, contrast)

---

## 🎨 Design System - Glassmorphism

### Visual Language:
- **Modern Glassmorphism** aesthetic
- **Frosted translucent panels** with subtle blur
- **Soft gradients** and depth
- **Minimal shadows** for practical contrast
- **Smooth microinteractions** (0.12-0.28s ease-out)

### Color Palette:
```
Glass Base: rgba(255,255,255,0.07)
Foreground: rgba(255,255,255,0.94)
Accent 1: #89B5FF (Primary actions)
Accent 2: #FFCF86 (Highlights)
Accent 3: #C5A6FF (Secondary)
Neutral: #11151C (Background)
Danger: #E86A6A
Success: #55D68D
```

### Typography:
- System font stacks
- Body: 16-18px
- Headings: 20-28px
- Semi-bold for primary CTAs
- High-contrast for data tables

### Components:
- **Glass Cards**: Frosted panels with subtle borders
- **Modals**: Centered with soft elevation
- **Slide-overs**: Right-side detail panels (480-720px)
- **Data Tables**: Minimal headers, zebra striping, hover effects
- **Kanban Cards**: Compact glass tiles with drag affordance
- **Forms**: Inline validation, smart autocomplete
- **Toasts**: Top-right notifications with glass background

---

## 🔄 Real-World Use Cases

### Use Case 1: Fixed-Price Project Lifecycle
1. **Planning**: Create project with budget and timeline
2. **Sales**: Create Sales Order with milestone-based line items
3. **Execution**: Create tasks, assign team, track progress
4. **Time Tracking**: Team logs hours per task
5. **Milestone Billing**: Generate customer invoice from SO lines
6. **Revenue Tracking**: Monitor actual revenue vs budget
7. **Profitability**: Analyze profit margin at project completion

### Use Case 2: Vendor Management
1. **Procurement**: Create Purchase Order for vendor services
2. **Work Delivery**: Vendor completes work
3. **Bill Receipt**: Record vendor bill linked to PO
4. **Cost Tracking**: Track actual costs against budget
5. **Profitability**: Calculate net profit (revenue - all costs)

### Use Case 3: Team Expense Workflow
1. **Submission**: Team member submits expense with receipt
2. **Review**: PM reviews expense details
3. **Approval**: PM approves expense
4. **Billing Decision**: Mark as billable if client-reimbursable
5. **Invoice Integration**: Add to customer invoice if billable
6. **Reimbursement**: Process payment to team member

### Use Case 4: Time & Materials Project
1. **Setup**: Create project with T&M Sales Order
2. **Work**: Team logs hours daily via timesheets
3. **Approval**: PM approves timesheets weekly
4. **Billing**: Generate invoice from approved timesheets
5. **Revenue**: Track cumulative revenue vs work performed

---

## 🔑 Key Terminologies

- **Sales Order (SO)**: Customer's purchase agreement; links to revenue
- **Purchase Order (PO)**: Company's purchase from vendor; links to costs
- **Customer Invoice**: Bill sent to customer; tracks income
- **Vendor Bill**: Bill received from supplier; tracks payables
- **Timesheet**: Work hours log; impacts project costs and billing
- **Expense**: Reimbursable cost; can be billable to customer
- **Milestone**: Project phase or deliverable; often linked to SO lines
- **Billable**: Can be charged to customer
- **Non-billable**: Internal cost not charged to customer
- **Cost Rate**: Internal hourly cost for resource
- **Profit Margin**: (Revenue - Costs) / Revenue

---

## 🎯 Core UX Principles

### 1. Progressive Disclosure
- Show high-level KPIs first
- Drill-down to details via modals/panels
- Avoid information overload

### 2. Fluent CRUD Operations
- In-context modals for Create/Edit
- Inline validation
- Single-click linking between entities

### 3. Data-First Design
- All UI anchored to database schema
- Complete field coverage in forms
- Metadata tracking (created_by, dates, status)

### 4. Safety & Confirmations
- Confirm destructive actions
- Optional reason field for deletions
- Undo capabilities where possible

### 5. Accessibility (WCAG AA)
- High contrast for important elements
- 44x44px minimum touch targets
- Logical tab order
- ARIA labels for complex widgets
- Keyboard-only navigation support
- Reduce motion toggle

### 6. Responsive Design
- Desktop-first 12-column grid
- Tablet: 2-column collapse
- Mobile: Stacked panels
- Touch-optimized controls

---

## 🚀 Key Features Summary

### Planning Features
✅ Project creation and management  
✅ Team assignment and roles  
✅ Task breakdown and dependencies  
✅ Milestone tracking  
✅ Budget planning and allocation  

### Execution Features
✅ Kanban board for visual task management  
✅ Task assignment and status tracking  
✅ Time logging with billable/non-billable  
✅ Collaborative comments and attachments  
✅ Blocker identification and resolution  

### Billing Features
✅ Sales Order creation and tracking  
✅ Purchase Order management  
✅ Customer invoice generation  
✅ Vendor bill processing  
✅ Expense submission and approval  
✅ Multi-currency support  
✅ Automated invoice line generation  

### Analytics Features
✅ Real-time project dashboards  
✅ Budget vs actual tracking  
✅ Profitability analysis per project  
✅ Resource utilization reports  
✅ Revenue and cost trending  
✅ Custom date range filtering  

### Collaboration Features
✅ Task comments and mentions  
✅ File attachments and previews  
✅ Activity timeline  
✅ Real-time notifications  
✅ Team member profiles  

---

## 📱 Screen Structure

### Main Screens:
1. **Dashboard** - Role-aware landing page with KPIs
2. **Projects List** - All projects with filters and search
3. **Project Detail** - Tabbed view (Overview, Tasks, Board, Financials, Team)
4. **Tasks** - My Tasks / All Tasks with Kanban and list views
5. **Timesheets** - Calendar and table views for time tracking
6. **Sales & Purchases** - Global lists for financial documents
7. **Analytics** - Comprehensive reporting and charts
8. **Settings** - Users, products, partners, system config

### Detail Views (Modals/Slide-overs):
- Task Detail
- Project Members
- Create/Edit Forms (Projects, Tasks, SO, PO, Invoices, Bills)
- Financial Document Details

---

## 🔐 Security & Data Integrity

- **Role-based Access Control** (RBAC)
- **Field-level Permissions**
- **Audit Trail** (created_by, updated_at tracking)
- **Secure Password Hashing**
- **Session Management**
- **Data Validation** (client and server-side)
- **Referential Integrity** via foreign keys
- **Transaction Safety** for financial operations

---

## 📊 Data Relationships

### Core Entity Relationships:
- **Projects** → many Tasks, Sales Orders, Purchase Orders, Invoices, Bills, Expenses, Timesheets
- **Tasks** → many Assignments (users), Comments, Attachments, Timesheets
- **Sales Orders** → many Sales Order Lines → Customer Invoice Lines
- **Purchase Orders** → many Purchase Order Lines → Vendor Bill Lines
- **Timesheets** → one Task, one User, optional Invoice Line
- **Expenses** → one Project, optional Task, optional Invoice Line
- **Users** → many Roles (many-to-many)
- **Projects** → many Members (users with project roles)

---

## 🎓 Getting Started

### For Project Managers:
1. Create a new project with budget and dates
2. Invite team members
3. Create Sales Order with milestones
4. Break down work into tasks
5. Assign tasks to team
6. Monitor progress on dashboard
7. Approve timesheets and expenses
8. Generate invoices from completed work

### For Team Members:
1. View "My Tasks" on dashboard
2. Update task status as you work
3. Log hours daily via timesheets
4. Submit expenses with receipts
5. Add comments and collaborate
6. Upload relevant attachments

### For Sales/Finance:
1. Create Sales Orders for new deals
2. Create Purchase Orders for procurement
3. Generate invoices from SO lines or timesheets
4. Process vendor bills
5. Monitor financial health per project
6. Track revenue and profitability

### For Admins:
1. Set up users and assign roles
2. Configure products and pricing
3. Manage partners (customers/vendors)
4. Set hourly rates for employees
5. Monitor system-wide analytics
6. Configure global settings

---

## 📈 Workflow Automation

- **Auto-link Suggestions**: When creating invoices, suggest relevant timesheets and expenses
- **Invoice Generation Wizard**: Transform SO lines or timesheets into invoice lines
- **Multi-select Batch Operations**: Bulk approve timesheets, bulk assign tasks
- **Inline Conversions**: One-click convert SO line to invoice line
- **Audit Trail**: Automatic tracking of all changes

---

## 🎯 Success Metrics

- **Time to Create Project**: < 2 minutes
- **Task Status Update**: < 5 seconds
- **Timesheet Entry**: < 30 seconds per entry
- **Invoice Generation**: < 2 minutes from selection to draft
- **Dashboard Load Time**: < 2 seconds
- **Search Response**: < 1 second

---

## 📞 Support & Documentation

- **In-app Help**: Contextual tooltips and guides
- **Keyboard Shortcuts**: Quick actions for power users
- **FAQ Section**: Common questions and answers
- **Video Tutorials**: Step-by-step walkthroughs
- **API Documentation**: For custom integrations

---

## 🗺️ Roadmap

### Future Enhancements:
- Mobile applications (iOS/Android)
- Advanced resource scheduling
- Gantt chart visualization
- Email integration for notifications
- Third-party integrations (Slack, Jira, QuickBooks)
- AI-powered project insights
- Predictive budget analytics
- Custom report builder

---

## 📄 License

[Specify your license here]

---

## 👥 Contributors

[List contributors or link to CONTRIBUTORS.md]

---

## 🙏 Acknowledgments

Built with modern web technologies and best practices from:
- Apple Human Interface Guidelines
- Google Material Design
- Glassmorphism design principles
- WCAG accessibility standards

---

**OneFlow** - Where Planning meets Execution meets Billing. All in one beautiful, intuitive platform.
