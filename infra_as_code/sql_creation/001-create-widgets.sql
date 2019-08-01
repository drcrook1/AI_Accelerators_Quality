CREATE TABLE [dbo].[classified_widgets](
	[serial_number] [nvarchar](50) NULL,
	[std_dist] [float] NULL,
	[std] [float] NULL,
	[mean] [float] NULL,
	[threshold] [float] NULL,
	[is_good] [bit] NULL,
	[id] [nvarchar](200) NOT NULL,
	[factory_id] [nvarchar](50) NOT NULL,
	[line_id] [nvarchar](50) NOT NULL,
	[classified_time] [datetime2] NOT NULL,
 CONSTRAINT [PK_classified_widgets] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)
)
