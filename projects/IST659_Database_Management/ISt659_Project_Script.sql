USE [IST659_Project]
GO
/****** Object:  Table [dbo].[attendance]    Script Date: 3/28/2020 11:46:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[attendance](
	[attend_geo_location] [nvarchar](255) NOT NULL,
	[photo_url] [float] NULL,
	[action] [nvarchar](255) NOT NULL,
	[attend_time] [nvarchar](255) NOT NULL,
	[attend_comment] [float] NULL,
	[attend_id] [nvarchar](255) NOT NULL,
	[user_id] [nvarchar](255) NOT NULL,
	[F8] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[attend_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Company]    Script Date: 3/28/2020 11:46:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Company](
	[company_id] [nvarchar](255) NOT NULL,
	[company_name] [nvarchar](255) NOT NULL,
	[display_name] [nvarchar](255) NULL,
	[company_type] [nvarchar](255) NOT NULL,
	[company_status] [nvarchar](255) NOT NULL,
	[company_city] [nvarchar](255) NOT NULL,
	[company_country] [nvarchar](255) NOT NULL,
	[company_address] [nvarchar](255) NULL,
	[company_email_address] [nvarchar](255) NOT NULL,
	[max_tags] [float] NOT NULL,
	[company_create_date] [datetime] NULL,
	[company_update_date] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[company_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[incidents]    Script Date: 3/28/2020 11:46:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[incidents](
	[incident_geo_location] [nvarchar](255) NOT NULL,
	[incident_comments] [nvarchar](255) NOT NULL,
	[report_time] [nvarchar](255) NOT NULL,
	[incident_id] [nvarchar](255) NOT NULL,
	[site_id] [nvarchar](255) NOT NULL,
	[incident_photo_url] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[incident_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Site]    Script Date: 3/28/2020 11:46:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Site](
	[site_id] [nvarchar](255) NOT NULL,
	[site_name] [nvarchar](255) NOT NULL,
	[company_id] [nvarchar](255) NOT NULL,
	[isAdmin] [float] NOT NULL,
	[isGroup] [float] NOT NULL,
	[site_type] [nvarchar](255) NOT NULL,
	[site_address] [nvarchar](255) NULL,
	[site_city] [nvarchar](255) NOT NULL,
	[scan_starthour] [float] NOT NULL,
	[scan_endhour] [float] NOT NULL,
	[scan_interval] [float] NOT NULL,
	[site_create_date] [datetime] NULL,
	[site_update_date] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[site_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tags]    Script Date: 3/28/2020 11:46:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tags](
	[tag_name] [nvarchar](255) NOT NULL,
	[tag_id] [float] NOT NULL,
	[tag_location] [nvarchar](255) NULL,
	[comment] [nvarchar](255) NULL,
	[tag_create_date] [datetime] NULL,
	[tag_update_date] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[tag_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tagscans]    Script Date: 3/28/2020 11:46:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tagscans](
	[geo_location] [nvarchar](255) NOT NULL,
	[scan_type] [nvarchar](255) NOT NULL,
	[scanTime] [nvarchar](255) NOT NULL,
	[SSID] [nvarchar](255) NULL,
	[tag_scan_id] [nvarchar](255) NOT NULL,
	[site_id] [nvarchar](255) NOT NULL,
	[tag_id] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[tag_scan_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[user_profile]    Script Date: 3/28/2020 11:46:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[user_profile](
	[user_id] [nvarchar](255) NOT NULL,
	[site_id] [nvarchar](255) NOT NULL,
	[user_name] [nvarchar](255) NOT NULL,
	[user_email_address] [nvarchar](255) NOT NULL,
	[first_name] [nvarchar](255) NULL,
	[last_name] [nvarchar](255) NULL,
	[user_phone] [nvarchar](255) NULL,
	[user_photo_url] [nvarchar](255) NULL,
	[user_create_date] [datetime] NULL,
	[user_update_date] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[user_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
